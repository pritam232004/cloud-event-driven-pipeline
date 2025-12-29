import json
import boto3
import datetime

s3 = boto3.client('s3')
BUCKET_NAME = "event-driven-data-bucket"

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        timestamp = datetime.datetime.utcnow().isoformat()
        file_name = f"raw/event_{timestamp}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=json.dumps(body)
        )

        return {
            "statusCode": 200,
            "body": json.dumps("Event stored successfully")
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps("Error storing event")
        }
