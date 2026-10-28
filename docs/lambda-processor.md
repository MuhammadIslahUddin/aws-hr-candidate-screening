# Lambda Processor — Initial Implementation

## Function

`hr-screening-cv-processor`

## Runtime

Python 3.12, if available in the selected AWS Region.

## Responsibilities

1. Receive SQS messages containing S3 event notifications.
2. Validate that the event references the expected S3 bucket.
3. Process object-created events.
4. Read the referenced object from S3.
5. Write an initial processing record to DynamoDB.
6. Return failed message identifiers for partial-batch retries.

## AWS Resources

- S3 bucket: `hr-screening-cv-uploads-islah-8291`
- SQS queue: `hr-screening-processing-queue`
- DynamoDB table: `hr-screening-candidates`

## Security

- Uses a Lambda execution role rather than embedded credentials.
- Restricts S3 reads to the designated bucket.
- Restricts DynamoDB writes to the candidate table.
- Does not log CV contents.
- Uses synthetic documents during development.

## Current Limitations

This version validates the event pipeline and database integration. It does not yet extract text from PDFs or DOCX files, detect personally identifiable information, calculate job-related scores, or use an AI model.

All AI-assisted assessments added later must support human review rather than automatically reject applicants.
