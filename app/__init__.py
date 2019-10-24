from app.api.restplus import api

from flask import Flask, Blueprint
import logging

from app.api.auth.endpoints import ns as ns_auth
from app.api.users.endpoints import ns as ns_users
from app.db.database import init_db
from app.utils.log import init_logger


def create_app():
    init_logger(__name__)
    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True

    if app.config["DEBUG"]:
        app.config.from_pyfile("./configs/dev.py")
    else:
        app.config.from_pyfile("./configs/dev.py")

    # to avoid Runtime error
    with app.app_context():
        init_db()

    blueprint = Blueprint("api", __name__, url_prefix="/api")
    api.init_app(blueprint)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_users)

    app.register_blueprint(blueprint)

    return app
