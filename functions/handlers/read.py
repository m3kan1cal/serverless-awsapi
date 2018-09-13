import os

import boto3

import functions.exceptions as ex
import functions.validator as val
from functions.beacon import respond
from functions.models.note import NoteModel


def read(event, context):
    """Read item from the collection."""

    try:
        
        # Determine if required env var for region is present.
        val.check_region()

        # Determine if required env var for DynamoDB table is present.
        val.check_dynamodb()

        # Check for the url {id}.
        note_id = val.check_id(event)

        # Set up resource and environment. This is where we keep
        # *aaS provider resources away from biz logic.
        region = os.environ["AWS_DEFAULT_REGION"]
        table = os.environ["DYNAMODB_TABLE"]
        
       # Determine which DynamoDB host we need (local/remote)?
        host = val.check_dynamodb_host()
        conn = boto3.resource("dynamodb", region, endpoint_url=host)
        conn_table = conn.Table(table)

        # Build our model and read.
        note = NoteModel(conn_table)
        item = note.read(note_id)

        return respond(200, item)
    
    except ex.AwsRegionNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.DynamoDbTableNotSetException as exc:
        return respond(500, {"error": str(exc)})

    except ex.RequestUrlIdNotSetException as exc:
        return respond(400, {"error": str(exc)})

    except Exception as exc:
        return respond(500, {"error": str(exc)})
