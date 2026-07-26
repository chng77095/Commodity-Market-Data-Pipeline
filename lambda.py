import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = 'cci-commodity-market-data-yourname'

def lambda_handler(event, context):
    processed_records = []

    # Process batch of records from SQS
    for record in event['Records']:
        body = json.loads(record['body'])

        # Real-time data validation
        last_price = body.get('last_price')
        if last_price is None or last_price <= 0:
            print(f"[ALERT] Invalid record skipped: {body}")
            continue

        body['data_quality_status'] = 'PASSED'
        processed_records.append(body)

    if processed_records:
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        file_key = f"validated_ticks/ticks_{timestamp}.json"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_key,
            Body=json.dumps(processed_records)
        )
        print(f"Saved {len(processed_records)} records to S3.")

    return {'statusCode': 200}
