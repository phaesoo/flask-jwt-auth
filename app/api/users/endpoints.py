from flask_restplus import Resource, reqparse, fields

import logging

from app.api.restplus import api

from app.models.auth import AuthUser
from datetime import datetime
from app.db.database import get_session

logger = logging.getLogger(__name__)

ns = api.namespace("users", description="Endpoints for user")


@ns.route("/")
class Root(Resource):
    def get(self):
        db = get_session("auth")
        data= db.query(AuthUser).one()
        print data.username
        
    def post(self):
        user = AuthUser(
            id=0,
            password="123",
            last_login=datetime.now(),
            is_superuser=False,
            username="hspark",
            first_name="Haesoo",
            last_name="Park",
            email="hspark@haafor.com",
            is_staff=False,
            is_active=True,
            date_joined=datetime.now()
        )
        print user
        db = get_session("auth")
        db.add(user)
        db.commit()

        logger.info("Get all user list")


@ns.route("/<username>")
class Username(Resource):
    def get(self, username):
        logger.info("Get user info: {}".format(username))

    def put(self, username):
        logger.info("put user info: {}".format(username))

    def delete(self, username):
        logger.info("delete user info: {}".format(username))
