from flask_restplus import Resource, reqparse, fields
from sqlalchemy.orm import load_only
import logging
from datetime import datetime

from app.api.restplus import api
from app.decorators.auth import jwt_authenticate
from app.models.auth import AuthUser
from app.db.database import get_session
from app.encrypt.encrypt import encrypt_sha
from app.response import response as resp
from app.utils.validate import check_username, check_password, check_email

logger = logging.getLogger(__name__)

ns = api.namespace("users", description="Endpoints for user")

parser_create = reqparse.RequestParser()
parser_create.add_argument("username", type=str, required=True)
parser_create.add_argument("password", type=str, required=True)
parser_create.add_argument("first_name", type=str, required=True)
parser_create.add_argument("last_name", type=str, required=True)
parser_create.add_argument("email", type=str, required=True) 


parser_update = reqparse.RequestParser()
parser_update.add_argument("password", type=str, required=True)
parser_update.add_argument("new_password", type=str)
parser_update.add_argument("first_name", type=str)
parser_update.add_argument("last_name", type=str)
parser_update.add_argument("email", type=str) 


@ns.route("")
class Root(Resource):
    @jwt_authenticate(is_superuser=True)
    def get(self, **kwargs):
        session = get_session("auth")
        obj_list= session.query(AuthUser).all()

        result = list()
        for auth_user in obj_list:
            result.append({
                "id": auth_user.id,
                "username": auth_user.username,
                "first_name": auth_user.first_name,
                "last_name": auth_user.last_name,
                "email": auth_user.email,
            })
        return resp.success(result)

    def post(self):
        try:
            parsed = parser_create.parse_args()
        except:
            return resp.error("Invalid request arguments")

        is_valid, err_msg = check_username(parsed.username)
        if not is_valid:
            return resp.error(err_msg)

        is_valid, err_msg = check_password(parsed.password)
        if not is_valid:
            return resp.error(err_msg)

        is_valid, err_msg = check_email(parsed.email)
        if not is_valid:
            return resp.error(err_msg)

        session = get_session("auth")
        if session.query(AuthUser).filter_by(username=parsed.username).count():
            return resp.error("Already existed username")

        try:
            user = AuthUser(
                username=parsed.username,
                password=encrypt_sha(parsed.password),
                last_login=datetime.now(),
                is_superuser=False,
                first_name=parsed.first_name,
                last_name=parsed.last_name,
                email=parsed.email,
                is_staff=False,
                is_active=True,
                date_joined=datetime.now()
            )
            session.add(user)
        except:
            session.rollback()
            return resp.error("Error while update user info.")
        else:
            session.commit()

        auth_user = session.query(AuthUser).filter_by(username=parsed.username).first()
        return resp.success({
            "id": auth_user.id,
            "username": auth_user.username,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "email": auth_user.email,
        })

@ns.route("/<username>")
class Username(Resource):
    @jwt_authenticate()
    def get(self, username, **kwargs):
        session = get_session("auth")
        auth_user = session.query(AuthUser).filter_by(username=username)[0]

        return resp.success({
            "id": auth_user.id,
            "username": auth_user.username,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "email": auth_user.email,
        })

    @jwt_authenticate()
    def put(self, username, **kwargs):
        try:
            parsed = parser_update.parse_args()
        except:
            return resp.error("Invalid request arguments")

        session = get_session("auth")
        auth_user = session.query(AuthUser).filter_by(username=username).first()
        if auth_user.password != encrypt_sha(parsed.password):
            return resp.error("Invalid password")

        update_dict = dict()
        new_password = parsed.get("new_password")
        if new_password is not None:
            is_valid, err_msg = check_password(new_password)
            if not is_valid:
                return resp.error(err_msg)
            
        for key in ["new_password", "first_name", "last_name", "email"]:
            val = parsed.get(key)
            if val is not None:
                if key == "new_password":
                    update_dict["password"] = val
                else:
                    update_dict[key] = val

        try:
            session.query(AuthUser).update(update_dict)
        except:
            session.rollback()
            return resp.error("Error while update user info.")
        else:
            session.commit()

        auth_user = session.query(AuthUser).filter_by(username=username).first()
        return resp.success({
            "id": auth_user.id,
            "username": auth_user.username,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "email": auth_user.email,
        })

    @jwt_authenticate(is_superuser=True)
    def delete(self, username, **kwargs):
        session = get_session("auth")

        auth_user = session.query(AuthUser).filter_by(username=username).first()

        try:
            session.query(AuthUser).filter_by(username=username).delete()
        except:
            session.rollback()
            return resp.error("Error while update user info.")
        else:
            session.commit()

        return resp.success({
            "id": auth_user.id,
            "username": auth_user.username,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "email": auth_user.email,
        })
