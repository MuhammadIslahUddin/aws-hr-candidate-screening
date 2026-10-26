# AWS HR Candidate Screening Platform

An end-to-end, serverless AWS application for processing synthetic CV documents, extracting job-related information, evaluating candidate qualifications, and notifying recruiters.

## Architecture

Amazon S3, Amazon SQS, AWS Lambda, Amazon Textract, Amazon Comprehend, Amazon Bedrock, Amazon DynamoDB, Amazon SNS, Amazon Cognito, Amazon API Gateway, AWS Amplify, Amazon CloudWatch, and AWS CloudTrail.

## Key Engineering Goals

- Secure document storage and encryption
- Asynchronous, event-driven processing
- AI-assisted information extraction
- Job-related candidate evaluation with human review
- Centralized logging and monitoring
- Cost-conscious AWS resource management
- Reproducible documentation and testing

## Infrastructure Approach

AWS resources are configured through the AWS Management Console. Application logic is implemented in code. Terraform, AWS CDK, and infrastructure deployment templates are not used.

## Data Privacy

This project uses synthetic CVs only. It is a portfolio demonstration, not a validated hiring decision system.

## Project Status

In development.
