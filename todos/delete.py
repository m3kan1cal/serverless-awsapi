import os

import boto3

dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    """Delete item in the collection."""

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Delete the item from the database.
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # Create a response.
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
    }

    return response
