import os
import time

import pytest
from pytest_mock import mocker
from moto import mock_dynamodb2

from functions.models.note import NoteModel
from tests.unit import dynamodb_table
from tests.unit import config


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
def test_read_returns_valid_structure_when_valid_data(dynamodb_table):
    model = NoteModel(dynamodb_table)
    created = model.save(user_id=test_globals["user_id"], notebook=test_globals["notebook"],
                      text=test_globals["text"])
    
    test_globals["note_id"] = created["noteId"]
    test_globals["user_id"] = created["userId"]
    test_globals["notebook"] = created["notebook"]
    test_globals["text"] = created["text"]
    test_globals["created_at"] = created["createdAt"]
    test_globals["updated_at"] = created["updatedAt"]

    item = model.read(test_globals["note_id"])

    assert "noteId" in item and item["noteId"] == test_globals["note_id"]
    assert "userId" in item and item["userId"] == test_globals["user_id"]
    assert "notebook" in item and item["notebook"] == test_globals["notebook"]
    assert "text" in item and item["text"] == test_globals["text"]

    assert "createdAt" in item and item["createdAt"] == test_globals["created_at"]
    assert "updatedAt" in item and item["updatedAt"] == test_globals["updated_at"]


@mock_dynamodb2
def test_read_returns_valid_structure_when_invalid_data(dynamodb_table):
    model = NoteModel(dynamodb_table)
    item = model.read(test_globals["note_id"] + "_badid")

    assert "noteId" not in item
    assert "userId" not in item
    assert "notebook" not in item
    assert "text" not in item

    assert "createdAt" not in item
    assert "updatedAt" not in item
