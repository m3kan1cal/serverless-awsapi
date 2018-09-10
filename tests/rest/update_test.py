import requests
import os
import time
import json

import pytest
import mock

import functions.validator as val
from tests.rest import api_notes_url


# Module scoped variables for simple unit testing.
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


def test_update_returns_valid_note_values_when_valid_data(api_notes_url):
    res = requests.post(api_notes_url, json={
                        "userId": test_globals["user_id"], "notebook": test_globals["notebook"],
                        "text": test_globals["text"]})
    created = res.json()
    
    test_globals["note_id"] = created["noteId"]
    test_globals["user_id"] = created["userId"]
    test_globals["notebook"] = created["notebook"]
    test_globals["text"] = created["text"]
    test_globals["created_at"] = created["createdAt"]
    test_globals["updated_at"] = created["updatedAt"]
    
    res = requests.put(
        "{0}/{1}".format(api_notes_url, test_globals["note_id"]),
        json={"userId": test_globals["user_id"], "notebook": test_globals["notebook"],
              "text": "Rest API test task updated"})
    payload = res.json()

    assert res.status_code == 200

    assert "noteId" in payload and payload["noteId"] == test_globals["note_id"]
    assert "userId" in payload and payload["userId"] == test_globals["user_id"]
    assert "notebook" in payload and payload["notebook"] == test_globals["notebook"]
    assert "text" in payload and payload["text"] == "Rest API test task updated"

    assert val.is_timestamp(payload["createdAt"]) == True
    assert val.is_timestamp(payload["updatedAt"]) == True

    assert "createdAt" in payload and payload["createdAt"] == test_globals["created_at"]
    assert "updatedAt" in payload and payload["updatedAt"] > test_globals["updated_at"]

    test_globals["text"] = payload["text"]
    test_globals["updated_at"] = payload["updatedAt"]


def test_update_returns_valid_note_values_when_invalid_data(api_notes_url):
    res = requests.put(
        "{0}/{1}".format(api_notes_url, test_globals["note_id"] + "_badid"),
        json={"userId": test_globals["user_id"], "notebook": test_globals["notebook"],
              "text": "Rest API test task updated"})
    payload = res.json()

    assert res.status_code == 200

    assert "noteId" not in payload
    assert "userId" not in payload
    assert "notebook" not in payload
    assert "text" not in payload

    assert "createdAt" not in payload
    assert "updatedAt" not in payload


def test_update_returns_status_code_400_when_request_body_not_json(api_notes_url):
    res = requests.put("{0}/{1}".format(api_notes_url, test_globals["note_id"]), 
                        data=bytes("some bytes", "utf8"))
    
    assert res.status_code == 400


def test_update_returns_status_code_400_when_required_props_not_set(api_notes_url):
    res = requests.put(
        "{0}/{1}".format(api_notes_url, test_globals["note_id"]), 
        json={"userId": test_globals["user_id"], "notebook": test_globals["notebook"],
              "badProp": test_globals["text"]})

    assert res.status_code == 400
