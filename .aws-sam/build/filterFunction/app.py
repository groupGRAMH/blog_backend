import json

# import requests


def lambda_handler(event, context):
    
      return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "working now bracn workflowgit",
            # "location": ip.text.replace("\n", "")
        }),
    }
