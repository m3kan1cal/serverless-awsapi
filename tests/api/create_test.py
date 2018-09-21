import requests
import os
import json

import pytest

import functions.validator as val
from tests.api import api_notes_url


# Module scoped variables for simple unit testing.
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


def test_create_returns_valid_note_values_when_valid_data(api_notes_url):
    res = requests.post(api_notes_url, json={
                        "userId": test_globals["user_id"], "notebook": test_globals["notebook"],
                        "text": test_globals["text"]})
    payload = res.json()

    assert res.status_code == 201

    assert "noteId" in payload
    assert "userId" in payload and payload["userId"] == test_globals["user_id"]
    assert "notebook" in payload and payload["notebook"] == test_globals["notebook"]
    assert "text" in payload and payload["text"] == test_globals["text"]

    assert "createdAt" in payload and val.is_now(int(payload["createdAt"]))
    assert "updatedAt" in payload and val.is_now(int(payload["updatedAt"]))

    test_globals["note_id"] = payload["noteId"]
    test_globals["user_id"] = payload["userId"]
    test_globals["notebook"] = payload["notebook"]
    test_globals["text"] = payload["text"]
    test_globals["created_at"] = payload["createdAt"]
    test_globals["updated_at"] = payload["updatedAt"]


def test_create_returns_status_code_400_when_request_body_not_json(api_notes_url):
    res = requests.post(api_notes_url, data=bytes("some bytes", "utf8"))
    
    assert res.status_code == 400


def test_create_returns_status_code_400_when_required_props_not_set(api_notes_url):
    res = requests.post(api_notes_url, json={
                        "userId": test_globals["user_id"], "notebook": test_globals["notebook"],
                        "badProp": test_globals["text"]})

    assert res.status_code == 400
