
class AwsRegionNotSetException(Exception):
    """Raised when no default AWS region is set in the environment variables."""
    pass


class DynamoDbTableNotSetException(Exception):
    """Raised when no DynamoDB table is set in the environment variables."""
    pass


class RequestBodyNotSetException(Exception):
    """Raised when no request body is set in the API request."""
    pass


class RequestBodyNotJsonException(Exception):
    """Raised when request body is not JSON in the API request."""
    pass


class RequiredPropertiesNotSetException(Exception):
    """Raised when request body JSON does not have required properties in the API request."""
    pass


class RequestUrlIdNotSetException(Exception):
    """Raised when request URI does not specific {id} in the API request."""
    pass
