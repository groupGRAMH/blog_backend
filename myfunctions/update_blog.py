import json
import boto3

dynamodb_table_name = 'BlogTable'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodb_table_name)

def update_handler(event, context):
    if event['httpMethod'] != 'PUT':
        raise Exception(f"updateMethod only accepts PUT method, you tried: {event['httpMethod']} method.")

    # Parse the request body
    body = json.loads(event['body'])

    # Check if the item ID is present in the request body
    if 'id' not in body:
        response = {
            'statusCode': 400,
            'body': json.dumps({'error': 'Item ID is required in the request body'})
        }
        return response

    item_id = body['id']

    # Fetch the existing item from DynamoDB
    try:
        response = table.get_item(Key={'id': item_id})
    except Exception as e:
        print("Error:", str(e))
        # Return an error response if retrieval fails
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to fetch item from DynamoDB'})
        }
        return response

    # Check if the item exists
    if 'Item' not in response:
        response = {
            'statusCode': 404,
            'body': json.dumps({'error': 'Item not found'})
        }
        return response

    # Update the item with the new values
    item = response['Item']
    item.update(body)

    # Put the updated item back into DynamoDB
    try:
        table.put_item(Item=item)
        print("Success - item updated")
    except Exception as e:
        print("Error:", str(e))
        # Return an error response if update fails
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to update item'})
        }
        return response

    # Prepare the success response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Item updated successfully'})
    }

    # All log statements are written to CloudWatch
    print(f"response from: {event['path']} statusCode: {response['statusCode']} body: {response['body']}")
    return response
