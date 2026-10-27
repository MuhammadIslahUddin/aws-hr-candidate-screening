# Database Architecture

## Amazon DynamoDB

The platform uses Amazon DynamoDB to store candidate screening records.

### Table

- **Table name:** `hr-screening-candidates`
- **Partition key:** `candidateId` (String)
- **Capacity mode:** On-demand
- **Encryption:** Default DynamoDB encryption at rest

### Global Secondary Index

- **Index name:** `jobId-score-index`
- **Partition key:** `jobId` (String)
- **Sort key:** `score` (Number)
- **Projection:** All attributes

### Example Record

The development environment uses synthetic candidate data only.

- `candidateId`: `test-001`
- `jobId`: `devops-engineer-01`
- `s3Key`: `candidate-001.txt`
- `status`: `SCORED`
- `score`: `78`
- `skills`: `Linux`, `Git`, `Docker`

This record validates the database structure; it is not a real candidate evaluation.

### Access Patterns

1. Retrieve a candidate by `candidateId` using the base table.
2. Retrieve candidates associated with a job using `jobId-score-index`.
3. Sort candidates by the numeric `score` within a job partition.

### Privacy and Responsible Use

- Only synthetic CVs are used during development.
- Candidate records must not be publicly accessible.
- Access should be restricted using IAM permissions.
- AI-generated evaluations are decision-support information only.
- A human recruiter must review the evidence before making hiring decisions.
