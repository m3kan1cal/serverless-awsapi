import logging

def setup_custom_logger(name):
    """Set up custom logger for specified namespace."""

    # Set up module logging levels and handlers.
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logging.getLogger("boto").setLevel(logging.ERROR)
    logging.getLogger("botocore").setLevel(logging.ERROR)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger