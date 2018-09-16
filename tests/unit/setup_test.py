import boto3
import pytest
from pytest_mock import mocker
# from moto import mock_dynamodb2

from tests.unit import dynamodb_table
from tests.unit import config

# @mock_dynamodb2
def test_setup_dependencies_when_tests_started(dynamodb_table):

    assert str(type(dynamodb_table)) == "<class 'boto3.resources.factory.dynamodb.Table'>"
