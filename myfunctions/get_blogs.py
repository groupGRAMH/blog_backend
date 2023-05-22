import json
import boto3
from decimal import Decimal

dynamodb_table_name = 'BlogTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def get_handler(event, context):
    if event['httpMethod'] != 'GET':
        raise Exception(f"getMethod only accepts GET method, you tried: {event['httpMethod']} method.")

    response = table.scan()
    items = response.get('Items', [])

    # Convert Decimal objects to string representation
    serialized_items = []
    for item in items:
        serialized_item = {k: str(v) if isinstance(v, Decimal) else v for k, v in item.items()}
        serialized_items.append(serialized_item)

    body = {
        'blogs': serialized_items
    }

    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }

  
    print(f"response from: {event['path']} statusCode: {response['statusCode']} body: {response['body']}")
    return response
