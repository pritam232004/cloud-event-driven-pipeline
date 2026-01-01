import json
import boto3
import uuid
from datetime import datetime

s3 = boto3.client("s3")

BUCKET_NAME = "event-driven-data-bucket232004"

def lambda_handler(event, context):
    data = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": "user_signup",
        "user_id": "user_123"
    }

    key = f"raw/{data['event_id']}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(data)
    )

    return {
        "statusCode": 200,
        "body": "Event stored successfully"
    }
