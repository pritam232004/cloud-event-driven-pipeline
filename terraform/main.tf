data "archive_file" "ingest_zip" {
  type        = "zip"
  source_file = "../lambda/ingest_lambda.py"
  output_path = "ingest.zip"
}

data "archive_file" "report_zip" {
  type        = "zip"
  source_file = "../lambda/report_lambda.py"
  output_path = "report.zip"
}


provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "event-driven-data-bucket232004"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_lambda_function" "ingest_lambda" {
  function_name    = "ingest_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "ingest_lambda.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.ingest_zip.output_path
  source_code_hash = data.archive_file.ingest_zip.output_base64sha256
}


resource "aws_lambda_function" "report_lambda" {
  function_name    = "report_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "report_lambda.lambda_handler"
  runtime          = "python3.9"
  filename         = data.archive_file.report_zip.output_path
  source_code_hash = data.archive_file.report_zip.output_base64sha256
}


resource "aws_cloudwatch_event_rule" "daily_rule" {
  schedule_expression = "rate(1 day)"
}

resource "aws_cloudwatch_event_target" "daily_target" {
  rule = aws_cloudwatch_event_rule.daily_rule.name
  arn  = aws_lambda_function.report_lambda.arn
  
}
