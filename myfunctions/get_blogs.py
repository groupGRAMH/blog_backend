import boto3
import json
from custom_encoder import CustomEncoder 
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'simple_table'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
getBlogPath = '/blog'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == getBlogPath:
        response = getBlogs()
    else:
        response = buildResponse(404, 'NotFound')
    
    return response
    
def getBlogs():
    try:
        response = table.scan()
        result = response['Items']
        
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])
        
        body = {
            'cars': result
        }
        return buildResponse(200, body)
    
    except:
        logger.exception('Do custom error handlin here')
        
def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            }
        }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response
