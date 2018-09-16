import os
import time
import json

import yaml
import pytest
import boto3

from functions.handlers.create import create
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


def test_create_returns_valid_response_structure_when_valid_data(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    response = create(http_event, {})
    payload = json.loads(response["body"])

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 201
    assert "headers" in response
    assert "body" in response

    assert "noteId" in payload
    assert "userId" in payload
    assert "notebook" in payload
    assert "text" in payload

    assert "createdAt" in payload and val.is_now(int(payload["createdAt"]))
    assert "updatedAt" in payload and val.is_now(int(payload["updatedAt"]))

    test_globals["note_id"] = payload["noteId"]
    test_globals["user_id"] = payload["userId"]
    test_globals["notebook"] = payload["notebook"]
    test_globals["text"] = payload["text"]
    test_globals["created_at"] = payload["createdAt"]
    test_globals["updated_at"] = payload["updatedAt"]


def test_create_returns_status_code_500_when_aws_region_not_set(monkeypatch, http_event, config):
    monkeypatch.delenv("AWS_DEFAULT_REGION", raising=False)
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)
    
    response = create(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_create_returns_status_code_500_when_dynamodb_table_not_set(monkeypatch, http_event, config):
    monkeypatch.delenv("DYNAMODB_TABLE", raising=False)
    
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    response = create(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 500


def test_create_returns_status_code_400_when_request_body_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    response = create(http_event.pop("body"), {})
    
    assert "statusCode" in response and response["statusCode"] == 400


def test_create_returns_status_code_400_when_request_body_not_json(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["body"] = bytes("some bytes", "utf8")
    response = create(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 400


def test_create_returns_status_code_400_when_required_props_not_set(monkeypatch, http_event, config):
    monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
    monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

    http_event["body"] = "{ \"userId\": \"azrael\", \"notebook\": \"system\", \"badProp\": \"Create handler test\" }"
    response = create(http_event, {})
    
    assert "statusCode" in response and response["statusCode"] == 400
