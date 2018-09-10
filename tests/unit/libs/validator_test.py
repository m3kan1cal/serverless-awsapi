import os
import time

import mock
import pytest
import yaml

from tests.unit import config, http_event
import functions.exceptions as ex
import functions.validator as val


def test_raises_exception_when_env_var_region_not_found(monkeypatch):
    with pytest.raises(ex.AwsRegionNotSetException) as exc:
        val.check_region()

        assert "'AWS_DEFAULT_REGION'" in str(exc.value)


def test_raises_exception_when_env_var_dynamodb_not_found(monkeypatch, config):
    with pytest.raises(ex.DynamoDbTableNotSetException) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
        val.check_dynamodb()

        assert "'DYNAMODB_TABLE'" in str(exc.value)


def test_raises_exception_when_body_property_not_found(monkeypatch, http_event, config):
    with pytest.raises(ex.RequestBodyNotSetException) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
        monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

        val.check_body(http_event.pop("body", None))

        assert "'body'" in str(exc.value)


def test_raises_exception_when_body_property_not_json(monkeypatch, http_event, config):
    with pytest.raises(ex.RequestBodyNotJsonException) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
        monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

        http_event["body"] = "Body that isn't JSON"
        val.check_json(http_event)

        assert "'JSON'" in str(exc.value)


def test_raises_exception_when_request_id_not_found(monkeypatch, http_event, config):
    with pytest.raises(ex.RequestUrlIdNotSetException) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
        monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

        val.check_id(http_event.pop("pathParameters", None))

        assert "'pathParameters'" in str(exc.value)


def test_raises_exception_when_required_properties_not_found(monkeypatch, http_event, config):
    with pytest.raises(ex.RequiredPropertiesNotSetException) as exc:
        monkeypatch.setenv("AWS_DEFAULT_REGION", config["aws"]["region"])
        monkeypatch.setenv("DYNAMODB_TABLE", config["aws"]["dynamodb"]["table"])

        http_event["body"] = "{ \"badtext\": \"Testing if OSError or Exception is raised\" }"
        val.check_props(http_event)

        assert "required properties" in str(exc.value)


def test_now_timestamp_returns_true_when_current():
    now = int(time.time() * 1000) # +/- 5 seconds of now.
    
    assert val.is_now(now) == True


def test_now_timestamp_returns_false_when_stale_or_future():
    old = int(time.time() * 1000) - 6000 # Make 6 seconds old.
    new = int(time.time() * 1000) + 6000 # Make 6 seconds future.

    assert val.is_now(old) == False
    assert val.is_now(new) == False


def test_is_timestamp_returns_true_when_valid_timestamp():
    now = int(time.time() * 1000)

    assert val.is_timestamp(now) == True


def test_is_timestamp_returns_false_when_invalid_timestamp():
    
    assert val.is_timestamp(24) == False
