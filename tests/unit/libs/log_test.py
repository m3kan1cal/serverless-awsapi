import logging

import pytest

import functions.log as log


def test_logger_returns_valid_named_logger(monkeypatch):

    # Get our module logger.
    logger = log.setup_custom_logger("notes")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "notes"
    assert logger.getEffectiveLevel() == logging.INFO

    assert logger.hasHandlers() == True
    
    assert logger.isEnabledFor(logging.INFO) == True
