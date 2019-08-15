import logging
from flask_restplus import Api


logger = logging.getLogger(__name__)
api = Api(version="1.0.0", title="Flask-JWT-Auth Example")

@api.errorhandler
def default_error_handler(e):
    message = "An unhandled exception occurred."
    logger.exception(message)
    print ("=== ERROR: {}".format(e))

    if not app.debug:
        return {"message": message}, 500