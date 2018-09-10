import os
import time

import mock
import pytest
from moto import mock_dynamodb2
from pytest_mock import mocker

from tests.unit import config, dynamodb_table
import functions.validator as val
from functions.models.note import NoteModel

# Module scoped variables for simple unit testing.
test_globals = {
    "note_id": None,
    "user_id": "azrael",
    "notebook": "system",
    "text": "Rest API test task",
    "created_at": None,
    "updated_at": None
}


@mock_dynamodb2
def test_search_by_user_returns_valid_structure_when_valid_data(dynamodb_table):
    model = NoteModel(dynamodb_table)
    items = model.search_by_user(test_globals["user_id"])

    for item in items:
        assert "noteId" in item
        assert "userId" in item and item["userId"] == test_globals["user_id"]
        assert "notebook" in item
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item


@mock_dynamodb2
def test_search_by_notebook_returns_valid_structure_when_valid_data(dynamodb_table):
    model = NoteModel(dynamodb_table)
    items = model.search_by_notebook(test_globals["notebook"])

    for item in items:
        assert "noteId" in item
        assert "userId" in item
        assert "notebook" in item and item["notebook"] == test_globals["notebook"]
        assert "text" in item

        assert "createdAt" not in item
        assert "updatedAt" not in item
