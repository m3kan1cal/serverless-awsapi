import pytest
import mock
from pytest_mock import mocker

from moto import mock_dynamodb2
from todos.models.todo import ToDoModel


@pytest.fixture
def dynamodb_table(monkeypatch):
    import os
    import boto3
    import botocore

    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
    monkeypatch.setenv("DYNAMODB_TABLE", "caas-todos-dev")

    conn = boto3.resource("dynamodb", os.environ["AWS_DEFAULT_REGION"],
                          endpoint_url="http://localhost:8000")
    table = os.environ["DYNAMODB_TABLE"]

    try:
        conn_table = conn.create_table(
            TableName=table,
            KeySchema=[
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                },
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                },
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            }
        )
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            conn_table = conn.Table(table)

    return conn_table


@mock_dynamodb2
def test_save_puts_data_when_valid(dynamodb_table):
    model = ToDoModel(dynamodb_table, "Testing if item is null")
    item = model.save()

    assert item != None


@mock_dynamodb2
def test_save_returns_valid_structure(dynamodb_table):
    model = ToDoModel(dynamodb_table, "Testing if structure is valid")
    item = model.save()

    assert "id" in item
    assert "text" in item
    assert "checked" in item
    assert "createdAt" in item
    assert "updatedAt" in item
