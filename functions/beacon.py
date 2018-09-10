import json

from functions.decimalencoder import DecimalEncoder

def respond(status_code, payload):
    """Wrap up our response for API messaging."""

    try:
        body = json.dumps(payload, cls=DecimalEncoder)
    except TypeError as exc:
        raise exc
    
    response = {
        "isBase64Encoded": False,
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": body
    }

    return response