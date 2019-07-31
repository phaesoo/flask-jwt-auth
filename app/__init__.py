from app.api.restplus import api

from flask import Flask, Blueprint
import logging

from app.api.auth.endpoints import ns as ns_auth
from app.api.users.endpoints import ns as ns_users
from app.db.database import init_db, db_sessions
from app.utils.log import init_logger

init_logger(__name__)
app = Flask(__name__)
app.config['BUNDLE_ERRORS'] = True

if app.config["DEBUG"]:
    print "debug"
    app.config.from_pyfile("./configs/dev.py")
else:
    raise Exception

init_db()


@app.teardown_request
def shoutdown_session(exception=None):
    for session in db_sessions:
        db_sessions[session].remove()


def init_api(api):
    api.add_namespace(ns_auth)
    api.add_namespace(ns_users)


def initialize_app(flask_app):
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    init_api(api)
    flask_app.register_blueprint(blueprint)


initialize_app(app)