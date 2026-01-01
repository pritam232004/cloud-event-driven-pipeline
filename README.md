Event-Driven Data Processing Pipeline using AWS & Terraform


The system ingests JSON data, stores it in Amazon S3, and periodically generates a summarized report.


##  Workflow
1. GitHub Actions triggers Terraform
2. Terraform provisions AWS infrastructure
3. "ingest_lambda" stores JSON in S3 (`raw/`)
4. "report_lambda" processes data and saves output (`report/`)
5. EventBridge schedules daily report generation

