import json
import boto3
from datetime import datetime
import uuid

s3 = boto3.client("s3")
BUCKET_NAME = "event-driven-data-bucket232004"

def lambda_handler(event, context):
    data = {
        "order_id": str(uuid.uuid4()),
        "amount": 250,
        "timestamp": datetime.utcnow().isoformat()
    }

    file_key = f"raw/orders_{data['order_id']}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Order stored successfully",
            "file": file_key
        })
    }
