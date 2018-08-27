import json
import logging
import os
import boto3

from todos.models.todo import ToDoModel


def create(event, context):
    """Create item in the collection."""

    if "AWS_DEFAULT_REGION" not in os.environ:
        logging.error(
            "Validation failed: 'AWS_DEFAULT_REGION' env variable not set.")
        raise OSError(
            "Validation failed: 'AWS_DEFAULT_REGION' env variable not set.")
    
    if "DYNAMODB_TABLE" not in os.environ:
        logging.error(
            "Validation failed: 'DYNAMODB_TABLE' env variable not set.")
        raise OSError(
            "Validation failed: 'DYNAMODB_TABLE' env variable not set.")

    if "body" not in event:
        logging.error("Validation failed: 'body' not present in http event.")
        raise ValueError("Validation failed: 'body' not present in http event.")

    data = json.loads(event["body"])
    
    if "text" not in data:
        logging.error("Validation failed: 'text' not present in request body.")
        raise ValueError(
            "Validation failed: 'text' not present in request body.")

    # Set up resource and environment. This is where we keep
    # *aaS provider resources away from biz logic.
    region = os.environ["AWS_DEFAULT_REGION"]
    table = os.environ["DYNAMODB_TABLE"]
    conn = boto3.resource("dynamodb", region)
    conn_table = conn.Table(table)

    # Build our model and save.
    todo = ToDoModel(conn_table, data["text"])
    item = todo.save()

    # Create a response.
    response = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(item)
    }

    return response
