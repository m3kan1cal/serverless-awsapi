import os

import pytest
import mock
import boto3
import botocore
import yaml


@pytest.fixture
def config():
    file = os.path.join(os.path.dirname(__file__), os.pardir, "config.yml")
    with open(file, "r") as configfile:
        cfg = yaml.load(configfile)

    return cfg


@pytest.fixture
def http_event():
    event = {
        "path": "/test/hello",
        "headers": {},
        "pathParameters": {"id": None},
        "requestContext": {},
        "resource": "/{proxy+}",
        "httpMethod": "GET",
        "queryStringParameters": {},
        "stageVariables": {},
        "body": "{ \"userId\": \"azrael\", \"notebook\": \"system\", \"text\": \"Create handler test\" }"
    }

    return event


@pytest.fixture
def dynamodb_table(monkeypatch, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    conn = boto3.resource(
        "dynamodb", os.environ["AWS_DEFAULT_REGION"], endpoint_url="http://localhost:8000")
    table = os.environ["DYNAMODB_TABLE"]

    try:
        conn_table = conn.create_table(
            TableName=table,
            KeySchema=[
                {
                    "AttributeName": "noteId",
                    "KeyType": "HASH"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "noteId",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "userId",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "notebook",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            },
            GlobalSecondaryIndexes=[
                {
                    # To get all notes for a specified user.
                    "IndexName": "stoic-notes-dev-userid-noteid-index",
                    "KeySchema": [
                        {
                            "AttributeName": "userId",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "noteId",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "NonKeyAttributes": ["text", "notebook"],
                        "ProjectionType": "INCLUDE"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                },
                {
                    # To get all notes for a specified notebook.
                    "IndexName": "stoic-notes-dev-notebook-noteid-index",
                    "KeySchema": [
                        {
                            "AttributeName": "notebook",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "noteId",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "NonKeyAttributes": ["text", "userId"],
                        "ProjectionType": "INCLUDE"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                }
            ]
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            conn_table = conn.Table(table)

    return conn_table