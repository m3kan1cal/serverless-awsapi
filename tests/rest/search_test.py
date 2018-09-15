import requests
import os
import time
import json

import pytest

from tests.rest import api_users_url
from tests.rest import api_notebooks_url
import functions.validator as val


# Module scoped variables for simple unit testing.
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


def test_search_by_user_returns_valid_note_values_when_valid_data(api_users_url):
    res = requests.get("{0}/{1}/notes".format(api_users_url, test_globals["user_id"]))
    payload = res.json()

    assert res.status_code == 200

    for item in payload:
        assert "noteId" in item
        assert "userId" in item and item["userId"] == test_globals["user_id"]
        assert "notebook" in item
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item


def test_search_by_notebook_returns_valid_note_values_when_valid_data(api_notebooks_url):
    res = requests.get("{0}/{1}/notes".format(api_notebooks_url, test_globals["notebook"]))
    payload = res.json()

    assert res.status_code == 200

    for item in payload:
        assert "noteId" in item
        assert "userId" in item
        assert "notebook" in item and item["notebook"] == test_globals["notebook"]
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item
