from oms_backend.api.restplus import api

from flask import Flask, Blueprint
from flask_cors import CORS
import logging

from db.database import init_db, db_sessions
from utils.log import init_logger

init_logger(__name__)
app = Flask(__name__)
init_db()


@app.teardown_request
def shoutdown_session(exception=None):
    for session in db_sessions:
        db_sessions[session].remove()


def init_api():
    pass


def initialize_app(flask_app):
    blueprint = Blueprint("api", __name__, url_prefix="/api")
    CORS(blueprint)
    api.init_app(blueprint)
    init_api()
    flask_app.register_blueprint(blueprint)


initialize_app(app)