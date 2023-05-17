import json
import os
import boto3

dynamodb_table_name = os.environ['MY_DATABASE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def create_handler(event, context):
    if event['httpMethod'] != 'POST':
        raise Exception(f"postMethod only accepts POST method, you tried: {event['httpMethod']} method.")
    
    # All log statements are written to CloudWatch
    print('received:', event)
    
    # Get info from the body of the request
    body = json.loads(event['body'])
    id = body['id']
    name = body['name']
    surname = body['surname']
    
    params = {
        'TableName': dynamodb_table_name,
        'Item': {
            'id': id,
            'name': name,
            'surname': surname
        }
    }
    
    try:
        table.put_item(Item=params['Item'])
        print("Success - item added or updated")
    except Exception as e:
        print("Error:", str(e))
    
    response = {
        'statusCode': 200,
        'body': json.dumps(body)
    }
    
    # All log statements are written to CloudWatch
    print(f"response from: {event['path']} statusCode: {response['statusCode']} body: {response['body']}")
    return response
