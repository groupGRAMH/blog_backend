import json
import boto3

def delete_handler(event, context):
    # TODO implement
    client_dynamo=boto3.resource('dynamodb')
    table=client_dynamo.Table('BlogTable ')
    id=event['id'] # this will delete row with partition key
    try:
        response=table.delete_item(Key={"id":id})
        return "Done"
    except:
        raise