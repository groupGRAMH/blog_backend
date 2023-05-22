import json
import boto3

dynamodb_table_name = 'BlogTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def delete_handler(event, context):
    if event['httpMethod'] != 'DELETE':
        raise Exception(f"deleteMethod only accepts DELETE method, you tried: {event['httpMethod']} method.")

    # Parse the request body
    try:
        body = json.loads(event['body'])
        print("Parsed request body:", body)
    except json.JSONDecodeError as e:
        print("Error parsing request body:", str(e))
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request body'})
        }
        return response

    # Check if the item ID is present in the request body
    if 'id' not in body:
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Item ID is required in the request body'})
        }
        return response

    item_id = body['id']

    # Delete the item from DynamoDB
    try:
        response = table.delete_item(
            Key={
                'id': item_id
            }
        )
        print("Success - item deleted")
    except Exception as e:
        print("Error:", str(e))
        # Return an error response if deletion fails
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to delete item'})
        }
        return response

    # Prepare the success response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item deleted successfully'})
    }

    print(f"response from: {event['path']} statusCode: {response['statusCode']} body: {response['body']}")
    return response
