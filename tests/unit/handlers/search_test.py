import os
import time
import json

import yaml
import pytest
import mock
import boto3

from functions.handlers.search import search_by_user
from functions.handlers.search import search_by_notebook
from tests.unit import config
from tests.unit import http_event
import functions.validator as val


# Module scoped variables for simple unit testing.
# @todo How can we point at the local DynamoDB local instance for testing handler?
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


def test_search_by_user_returns_valid_response_structure_when_valid_data(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = test_globals["user_id"]
    response = search_by_user(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    for item in payload:
        assert "noteId" in item
        assert "userId" in item and item["userId"] == test_globals["user_id"]
        assert "notebook" in item
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item


def test_search_by_user_returns_valid_response_structure_when_invalid_data(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = test_globals["user_id"] + "_badid"
    response = search_by_user(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    for item in payload:
        assert "noteId" not in item
        assert "userId" not in item
        assert "notebook" not in item
        assert "text" not in item

        assert "updatedAt" not in item
        assert "createdAt" not in item


def test_search_by_user_returns_status_code_500_when_aws_region_not_set(monkeypatch, http_event, config):
    response = search_by_user(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_search_by_user_returns_status_code_500_when_dynamodb_table_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    response = search_by_user(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_search_by_user_returns_status_code_400_when_request_id_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = None
    response = search_by_user(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"]["id"] = ""
    response = search_by_user(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"] = ""
    response = search_by_user(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400


def test_search_by_notebook_returns_valid_response_structure_when_valid_data(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = test_globals["notebook"]
    response = search_by_notebook(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    for item in payload:
        assert "noteId" in item
        assert "userId" in item
        assert "notebook" in item and item["notebook"] == test_globals["notebook"]
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item


def test_search_by_notebook_returns_valid_response_structure_when_invalid_data(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = test_globals["notebook"] + "_badid"
    response = search_by_notebook(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response

    for item in payload:
        assert "noteId" not in item
        assert "userId" not in item
        assert "notebook" not in item
        assert "text" not in item

        assert "updatedAt" not in item
        assert "createdAt" not in item


def test_search_by_notebook_returns_status_code_500_when_aws_region_not_set(monkeypatch, http_event, config):
    response = search_by_notebook(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_search_by_notebook_returns_status_code_500_when_dynamodb_table_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    response = search_by_notebook(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_search_by_notebook_returns_status_code_400_when_request_id_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["pathParameters"]["id"] = None
    response = search_by_notebook(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"]["id"] = ""
    response = search_by_notebook(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400

    http_event["pathParameters"] = ""
    response = search_by_notebook(http_event, {})

    assert "statusCode" in response and response["statusCode"] == 400
