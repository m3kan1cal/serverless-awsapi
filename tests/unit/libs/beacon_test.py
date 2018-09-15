import os
import json

import yaml
import pytest

from functions.beacon import respond


def test_beacon_responds_with_valid_payload_when_valid_data(monkeypatch):
    res = respond(200, {"test": "dictionary"})
    
    assert "isBase64Encoded" in res and isinstance(res["isBase64Encoded"], bool)
    
    assert "statusCode" in res and isinstance(res["statusCode"], int)
    assert res["statusCode"] == 200
    
    assert "headers" in res and isinstance(res["headers"], dict)
    assert "Content-Type" in res["headers"] and res["headers"]["Content-Type"] == "application/json"

    assert "body" in res and isinstance(res["body"], str)
    assert json.loads(res["body"]) ==  {"test": "dictionary"}


def test_beacon_responds_with_valid_payload_when_invalid_data(monkeypatch):
    with pytest.raises(TypeError) as exc:
        respond(200, bytes("bad dictionary", "utf-8"))
        
        assert "is not JSON serializable" in str(exc.value)
