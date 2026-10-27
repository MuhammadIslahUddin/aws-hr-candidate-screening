# Amazon SQS Architecture

## Purpose

Amazon SQS provides asynchronous message delivery between CV uploads and the candidate-processing Lambda function.

## Queues

### Main Processing Queue

- Name: `hr-screening-processing-queue`
- Type: Standard
- Visibility timeout: 180 seconds
- Message retention: 4 days
- Long polling: 20 seconds
- Encryption: SSE-SQS

### Dead-Letter Queue

- Name: `hr-screening-processing-dlq`
- Type: Standard
- Message retention: 4 days
- Encryption: SSE-SQS

### Retry Configuration

The main queue uses the DLQ with a maximum receive count of 3.

Messages that repeatedly fail processing can be moved to the DLQ for troubleshooting.

## Planned Event Flow

1. A synthetic CV is uploaded to a private Amazon S3 bucket.
2. An S3 object-created event is delivered to the main SQS queue.
3. A Lambda function receives the message.
4. The processor validates the event and reads the synthetic CV from S3.
5. Subsequent processing stages extract and analyze the document.
6. The resulting record is written to DynamoDB.

## Security and Reliability

- Queue encryption is enabled using SSE-SQS.
- Queue access should be restricted using IAM and queue policies.
- Message bodies should contain object references and required metadata, not CV contents or unnecessary personal information.
- The processor must handle duplicate events safely.
- Failed messages should be investigated before being retried or redriven.

## Development Scope

The queues are provisioned through the AWS Management Console. No infrastructure-as-code tool is used for this project.
