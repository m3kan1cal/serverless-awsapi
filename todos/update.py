import json
import time
import logging
import os

from todos import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')


def update(event, context):
    """Update item in the collection."""

    data = json.loads(event['body'])
    if 'text' not in data or 'checked' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't update the todo item.")
        return

    timestamp = int(time.time() * 1000)
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Update the item in the database.
    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
            '#todo_text': 'text',
        },
        ExpressionAttributeValues={
            ':text': data['text'],
            ':checked': data['checked'],
            ':updatedAt': timestamp,
        },
        UpdateExpression='SET #todo_text = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # Create a response.
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
