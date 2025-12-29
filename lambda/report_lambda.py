import boto3
import json

s3 = boto3.client('s3')
BUCKET_NAME = "event-driven-data-bucket"

def lambda_handler(event, context):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="raw/")
    total_events = response.get('KeyCount', 0)

    report = {
        "total_events": total_events
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="reports/daily_report.json",
        Body=json.dumps(report)
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Daily report generated")
    }
