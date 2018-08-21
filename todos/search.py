import json
import requests
import boto3


def search(event, context):
    """Return the sample todos list collection."""
    
    users = requests.get("https://jsonplaceholder.typicode.com/users")
    
    body = {
        "message": users.json(),
        "input": event
    }
    
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": { "Content-Type": "application/json" },
        "body": json.dumps(body)
    }

    return response
