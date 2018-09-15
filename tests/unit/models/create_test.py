import os
import time

import pytest
from pytest_mock import mocker
from moto import mock_dynamodb2

from functions.models.note import NoteModel
from tests.unit import dynamodb_table
from tests.unit import config
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


@mock_dynamodb2
def test_create_returns_valid_structure_when_valid_data(dynamodb_table):
    model = NoteModel(dynamodb_table)
    item = model.save(user_id=test_globals["user_id"], notebook=test_globals["notebook"],
                      text=test_globals["text"])

    assert "noteId" in item
    assert "userId" in item and item["userId"] == test_globals["user_id"]
    assert "notebook" in item and item["notebook"] == test_globals["notebook"]
    assert "text" in item and item["text"] == test_globals["text"]

    assert "createdAt" in item and val.is_now(int(item["createdAt"]))
    assert "updatedAt" in item and val.is_now(int(item["updatedAt"]))
