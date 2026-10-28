import json
import logging
import os
import urllib.parse
import uuid
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get(
    "CANDIDATES_TABLE",
    "hr-screening-candidates"
)

table = dynamodb.Table(TABLE_NAME)


def process_s3_event(event_record):
    """
    Process one S3 ObjectCreated event.

    The S3 notification is wrapped inside an SQS message.
    """
    bucket_name = event_record["s3"]["bucket"]["name"]
    object_key = urllib.parse.unquote_plus(
        event_record["s3"]["object"]["key"]
    )

    # Basic validation: only process objects from the expected bucket.
    expected_bucket = os.environ.get(
        "CV_BUCKET",
        "hr-screening-cv-uploads-islah-8291"
    )

    if bucket_name != expected_bucket:
        raise ValueError("Unexpected S3 bucket in event")

    logger.info(
        "Processing upload event for object key: %s",
        object_key
    )

    # Read the source object. Do not log its contents.
    response = s3.get_object(
        Bucket=bucket_name,
        Key=object_key
    )

    body = response["Body"]

    try:
        content = body.read()
    finally:
        body.close()

    # Use the S3 object key as a stable identifier for this
    # initial development test. We'll introduce proper candidate
    # and job identifiers in the next processing stages.
    candidate_id = str(uuid.uuid5(
        uuid.NAMESPACE_URL,
        f"s3://{bucket_name}/{object_key}"
    ))

    uploaded_at = datetime.now(
        timezone.utc
    ).isoformat()

    table.put_item(
        Item={
            "candidateId": candidate_id,
            "s3Key": object_key,
            "status": "UPLOADED",
            "uploadedAt": uploaded_at,
            "sourceBucket": bucket_name,
            "contentBytes": len(content),
            "summary": (
                "Synthetic development record. "
                "AI analysis has not yet been performed."
            )
        }
    )

    logger.info(
        "Created initial processing record for object key: %s",
        object_key
    )


def lambda_handler(event, context):
    failures = []

    for sqs_record in event.get("Records", []):
        message_id = sqs_record.get("messageId", "")

        try:
            message_body = json.loads(sqs_record["body"])

            # S3 can send a special test notification when
            # configuring event notifications. It has no Records.
            if message_body.get("Event") == "s3:TestEvent":
                logger.info("Received S3 test event")
                continue

            s3_records = message_body.get("Records", [])

            if not s3_records:
                raise ValueError(
                    "SQS message contains no S3 event records"
                )

            for s3_record in s3_records:
                if s3_record.get("eventSource") != "aws:s3":
                    raise ValueError(
                        "Unexpected event source"
                    )

                event_name = s3_record.get("eventName", "")

                if not event_name.startswith("ObjectCreated:"):
                    logger.info(
                        "Ignoring non-create event: %s",
                        event_name
                    )
                    continue

                process_s3_event(s3_record)

        except (ValueError, KeyError, json.JSONDecodeError):
            logger.exception(
                "Invalid SQS/S3 event. Message ID: %s",
                message_id
            )
            failures.append({
                "itemIdentifier": message_id
            })

        except ClientError:
            logger.exception(
                "AWS service error. Message ID: %s",
                message_id
            )
            failures.append({
                "itemIdentifier": message_id
            })

        except Exception:
            logger.exception(
                "Unexpected processing error. Message ID: %s",
                message_id
            )
            failures.append({
                "itemIdentifier": message_id
            })

    return {
        "batchItemFailures": failures
    }
