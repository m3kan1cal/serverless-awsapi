import os
import json

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')


def get(event, context):
    """Get item from the collection."""

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Fetch item from the database.
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # Create a response.
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
