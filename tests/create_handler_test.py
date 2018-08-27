import boto3
import os
import json

import pytest
import mock

from todos.create import create


@pytest.fixture
def http_event():
    event = {
        "path": "/test/hello",
        "headers": {},
        "pathParameters": {},
        "requestContext": {},
        "resource": "/{proxy+}",
        "httpMethod": "GET",
        "queryStringParameters": {},
        "stageVariables": {},
        "body": "{ \"text\": \"Testing if OSError or Exception is raised\" }"
    }

    return event


def test_raises_exception_when_env_var_region_not_found(monkeypatch, http_event):
    with pytest.raises(OSError) as exc:
        create(http_event, {})

        assert "'AWS_DEFAULT_REGION'" in str(exc.value)


def test_raises_exception_when_env_var_dynamodb_not_found(monkeypatch, http_event):
    with pytest.raises(OSError) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")

        create(http_event, {})

        assert "'DYNAMODB_TABLE'" in str(exc.value)


def test_raises_exception_when_request_body_not_found(monkeypatch, http_event):
    with pytest.raises(ValueError) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
        monkeypatch.setenv("DYNAMODB_TABLE", "caas-todos-dev")

        create(http_event.pop("body", None), {})

        assert "'body'" in str(exc.value)


def test_raises_exception_when_todo_text_not_found(monkeypatch, http_event):
    with pytest.raises(ValueError) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
        monkeypatch.setenv("DYNAMODB_TABLE", "caas-todos-dev")

        http_event["body"] = "{ \"badtext\": \"Testing if OSError or Exception is raised\" }"
        create(http_event, {})

        assert "'text'" in str(exc.value)


def test_create_returns_valid_response_structure_when_saved(monkeypatch, http_event):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
    monkeypatch.setenv("DYNAMODB_TABLE", "caas-todos-dev")

    response = create(http_event, {})

    assert "isBase64Encoded" in response and response["isBase64Encoded"] == False
    assert "statusCode" in response and response["statusCode"] == 200
    assert "headers" in response
    assert "body" in response


def test_create_returns_valid_todo_values_when_saved(monkeypatch, http_event):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-west-2")
    monkeypatch.setenv("DYNAMODB_TABLE", "caas-todos-dev")

    response = create(http_event, {})

    assert "id" in response["body"]
    assert "text" in response["body"]
    assert "checked" in response["body"]
    assert "createdAt" in response["body"]
    assert "updatedAt" in response["body"]
