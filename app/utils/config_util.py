from flask import current_app as app
import logging


logger = logging.getLogger(__name__)


def get_config(key):
    value = app.config.get(key)
    if value is None:
        logger.error("Trying to get undefined config: {}".format(key))
        raise ValueError
    return value
