import json
import boto3

dynamodb_table_name = 'BlogTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def get_handler(event, context):
    if event['httpMethod'] != 'GET':
        raise Exception(f"getMethod only accepts GET method, you tried: {event['httpMethod']} method.")

    
    response = table.scan()

    items = response.get('Items', [])

    
    body = {
        'blogs': items
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

    # All log statements are written to CloudWatch
    print(f"response from: {event['path']} statusCode: {response['statusCode']} body: {response['body']}")
    return response
