import json
import os
import boto3

dynamodb_table_name = os.environ['BlogTable']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path = event['path']
    
    if http_method == 'POST' and path == '/create':
        try:
            insert_blog(json.loads(event['body']))
            response = {
                'statusCode': 200,
                'body': json.dumps({
                    'Operation': 'SAVE',
                    'Message': 'SUCCESS',
                    'Item': json.loads(event['body'])
                })
            }
        except Exception as e:
            response = {
                'statusCode': 500,
                'body': json.dumps({
                    'error': str(e)
                })
            }
    else:
        response = {
            'statusCode': 404,
            'body': json.dumps({
                'error': 'NotFound'
            })
        }
    
    return response

def insert_blog(request_body):
    try:
        table.put_item(Item=request_body)
    except Exception as e:
        # Custom error handling
        raise Exception('Custom error handling here: ' + str(e))
