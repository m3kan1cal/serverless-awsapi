import json
import logging
import os
import re
import time
from datetime import datetime

import functions.exceptions as ex


def check_region():
    """Determine if required env var for region is present."""

    if "AWS_DEFAULT_REGION" not in os.environ:
        logging.error(
            "Validation failed: 'AWS_DEFAULT_REGION' env variable not set.")
        raise ex.AwsRegionNotSetException(
            "Validation failed: 'AWS_DEFAULT_REGION' env variable not set.")


def check_dynamodb():
    """Determine if required env var for DynamoDB table is present."""

    if "DYNAMODB_TABLE" not in os.environ:
        logging.error(
            "Validation failed: 'DYNAMODB_TABLE' env variable not set.")
        raise ex.DynamoDbTableNotSetException(
            "Validation failed: 'DYNAMODB_TABLE' env variable not set.")


def check_body(event):
    """Determine if required property body is present."""

    if "body" not in event:
        logging.error("Validation failed: 'body' not present in http event.")
        raise ex.RequestBodyNotSetException(
            "Validation failed: 'body' not present in http event.")


def check_json(event):
    """Attempt to parse JSON."""

    try:
        return json.loads(event["body"])
    except ValueError:
        logging.error("Validation failed: Could not parse JSON body.")
        raise ex.RequestBodyNotJsonException(
            "Validation failed: Could not parse JSON body.")


def check_id(event):
    """Determine if URI path {id} present."""

    url_id = None
    
    try:
        url_id = event["pathParameters"]["id"]

    except (ValueError, KeyError):
        logging.error(
            "Validation failed: 'id' not in a valid format or missing.")
        raise ex.RequestUrlIdNotSetException(
            "Validation failed: 'id' not in a valid format or missing.")
    
    finally:
        if url_id is not None and url_id is not "":
            return url_id
        
        else:
            logging.error(
                "Validation failed: 'id' not in a valid format or missing.")
            raise ex.RequestUrlIdNotSetException(
                "Validation failed: 'id' not in a valid format or missing.")


def check_props(data):
    """Determine if required properties are present."""

    if "userId" not in data or "notebook" not in data or "text" not in data:
        logging.error(
            "Validation failed: required properties (userId, notebook, text) not present in request body.")
        raise ex.RequiredPropertiesNotSetException(
            "Validation failed: required properties (userId, notebook, text) not present in request body.")


def check_dynamodb_host():
    """Determine the right DynamoDB host to use, local or remote."""

    if 'DYNAMODB_HOST' not in os.environ:
        return 'http://localhost:8000'
    else:
        return os.environ["DYNAMODB_HOST"]


def is_now(timestamp):
    """Determine if timestamp is +/- 10 seconds of now."""

    now = int(time.time() * 1000)
    return (now - 10000) <= timestamp <= (now + 10000)


def is_timestamp(timestamp):
    """Determine if timestamp is truly a valid timestamp in milliseconds."""

    if re.match("^[0-9]{13,13}$", str(timestamp)):
        return True
    else:
        return False
