from flask_restplus import Resource, reqparse, fields
from flask import jsonify
from sqlalchemy.orm import load_only
import logging
from datetime import datetime

from app.api.restplus import api
from app.decorators.auth import jwt_authenticate
from app.models.auth import AuthUser
from app.db.database import get_session
from app.encrypt.encrypt import encrypt_sha


logger = logging.getLogger(__name__)

ns = api.namespace("users", description="Endpoints for user")


parser = reqparse.RequestParser()
parser.add_argument("Authorization", type=str, location="headers", help="JWT", required=True)


@ns.route("")
class Root(Resource):
    @jwt_authenticate(is_superuser=True)
    def get(self, **kwargs):
        session = get_session("auth")
        obj_list= session.query(AuthUser).all()

        result = list()
        for auth_user in obj_list:
            result.append({
                "username": auth_user.username,
                "email": auth_user.email,
                "last_login": auth_user.last_login
            })
        return jsonify(result)

    def post(self):
        user = AuthUser(
            password=encrypt_sha("admin"),
            last_login=datetime.now(),
            is_superuser=True,
            username="administrator",
            first_name="Haesoo",
            last_name="Park",
            email="hspark@haafor.com",
            is_staff=False,
            is_active=True,
            date_joined=datetime.now()
        )
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
