import boto3

def lambda_handler(event, context):
    # Get the DynamoDB resource
    dynamodb = boto3.resource('dynamodb')
    
    # Get the table
    table_name = 'SampleTable'
    table = dynamodb.Table(table_name)
    
    # Get the key and updated value from the event
    key = event['key']
    updated_value = event['updated_value']
    
    try:
        # Update the item in DynamoDB
        response = table.update_item(
            Key={
                'id': key
            },
            UpdateExpression='SET your_attribute_name = :value',
            ExpressionAttributeValues={
                ':value': updated_value
            }
        )
        
        # Return the response
        return {
            'statusCode': 200,
            'body': 'Item updated successfully'
        }
    except Exception as e:
        # Return an error response
        return {
            'statusCode': 500,
            'body': str(e)
        }
