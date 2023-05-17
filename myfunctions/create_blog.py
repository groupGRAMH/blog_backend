import json
import boto3
import time

dynamodb_table_name = 'BlogTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

ALLOWED_CATEGORIES = ['technology', 'science', 'sports']

def validate_input(body):
    if 'author_name' not in body or not body['author_name']:
        raise Exception("author_name is required.")

    if 'author_surname' not in body or not body['author_surname']:
        raise Exception("author_surname is required.")

    if 'blog_title' not in body or not body['blog_title']:
        raise Exception("blog_title is required.")

    if 'blog_body' not in body or not body['blog_body']: 
        raise Exception("blog_body is required.")

    if 'blog_category' not in body or body['blog_category'] not in ALLOWED_CATEGORIES:
        raise Exception(f"blog_category is required and must be one of the following: {ALLOWED_CATEGORIES}")

def create_handler(event, context):
    if event['httpMethod'] != 'POST':
        raise Exception(f"postMethod only accepts POST method, you tried: {event['httpMethod']} method.")

    # set ELK
    print('received:', event)

    body = json.loads(event['body'])
    validate_input(body)

    author_name = body['author_name']
    author_surname = body['author_surname']
    blog_title = body['blog_title']
    blog_body = body['blog_body']
    blog_category = body['blog_category']
    views = 0
    create_at = int(time.time())

    params = {
        'TableName': dynamodb_table_name,
        'Item': {
            'id': str(create_at),
            'author_name': author_name,
            'author_surname': author_surname,
            'blog_category': blog_category,
            'blog_title': blog_title,
            'blog_body': blog_body,
            'views': views,
            'create_at': create_at
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
