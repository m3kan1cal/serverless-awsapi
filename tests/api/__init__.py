import os

import pytest
import boto3
import botocore
import yaml

@pytest.fixture
def api_notes_url():
    return "https://athena-dev.stoicapis.com/api/notes"


@pytest.fixture
def api_users_url():
    return "https://athena-dev.stoicapis.com/api/users"


@pytest.fixture
def api_notebooks_url():
    return "https://athena-dev.stoicapis.com/api/notebooks"
