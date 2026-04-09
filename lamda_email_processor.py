import boto3
import json
import email
from email import policy
from email.parser import BytesParser
import uuid
import time

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

TABLE_NAME = 'EmailMetadata'

def lambda_handler(event, context):
    """Processes new email from S3 and stores metadata in DynamoDB"""
    
    print(f"Full event: {json.dumps(event)}")
    
    try:
        # Get the S3 bucket and key from the event
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"Processing email from bucket: {bucket}, key: {key}")
        
        # Download raw email from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        raw_email = response['Body'].read()
        
        # Parse email
        msg = BytesParser(policy=policy.default).parsebytes(raw_email)
        
        # Extract metadata safely
        from_address = str(msg.get('From', 'Unknown'))
        to_address = str(msg.get('To', 'Unknown'))
        subject = str(msg.get('Subject', 'No Subject'))
        received_at = str(msg.get('Date', ''))
        
        # Generate a unique ID
        email_id = str(uuid.uuid4())
        
        email_metadata = {
            'email_id': email_id,
            'from_address': from_address,
            'to_address': to_address,
            'subject': subject,
            'timestamp': int(time.time()),
            'received_at': received_at,
            's3_bucket': bucket,
            's3_key': key
        }
        
        print(f"Metadata to save: {json.dumps(email_metadata)}")
        
        # Store in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=email_metadata)
        
        print(f"✅ Successfully processed email: {email_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Processed {email_id}")
        }
    
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }