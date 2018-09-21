import os

import boto3

import functions.log as log
import functions.exceptions as ex
import functions.validator as val

from functions.beacon import respond
from functions.models.note import NoteModel

# Get our module logger.
logger = log.setup_custom_logger("notes")


def create(event, context):
    """Create item in the collection."""

    try:

        # Determine if required env var for region is present.
        val.check_region()

        # Determine if required env var for DynamoDB table is present.
        val.check_dynamodb()

        # Determine if required property body is present.
        val.check_body(event)

        # Attempt to parse JSON.
        data = val.check_json(event)

        # Determine if required properties are present.
        val.check_props(data)

        # Set up resource and environment. This is where we keep
        # *aaS provider resources away from biz logic.
        region = os.environ["AWS_DEFAULT_REGION"]
        table = os.environ["DYNAMODB_TABLE"]

        # Determine which DynamoDB host we need (local/remote)?
        host = val.check_dynamodb_host()
        conn = boto3.resource("dynamodb", region, endpoint_url=host)
        conn_table = conn.Table(table)

        # Build our model and save.
        note = NoteModel(conn_table)
        item = note.save(data["userId"], data["notebook"], data["text"])

        logger.info("Note created: {}".format(item))
        return respond(201, item)

    except ex.AwsRegionNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.DynamoDbTableNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.RequestBodyNotSetException as exc:
        return respond(400, {"error": str(exc)})

    except ex.RequestBodyNotJsonException as exc:
        return respond(400, {"error": str(exc)})

    except ex.RequiredPropertiesNotSetException as exc:
        return respond(400, {"error": str(exc)})

    except Exception as exc:
        return respond(500, {"error": str(exc)})
