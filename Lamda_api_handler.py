import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailMetadata')

def lambda_handler(event, context):
    """Returns emails from DynamoDB - works for any GET request"""
    
    print(f"Event: {json.dumps(event)}")
    
    # For ANY GET request, return the emails
    # This bypasses all path matching issues
    try:
        response = table.scan()
        emails = response.get('Items', [])
        
        # Sort by timestamp (newest first)
        emails.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'count': len(emails),
                'emails': emails
            }, default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': False,
                'error': str(e)
            })
        }