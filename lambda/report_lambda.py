import json
import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "event-driven-data-bucket232004"

def lambda_handler(event, context):
    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="raw/"
    )

    count = response.get("KeyCount", 0)

    summary = {
        "total_events": count
    }

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key="reports/daily_summary.json",
        Body=json.dumps(summary)
    )

    return {
        "statusCode": 200,
        "body": "Report generated"
    }
