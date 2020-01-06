from flask_restplus import Resource, reqparse
import logging
from datetime import datetime

from app.api.restplus import api
from app.define import status
from app.db.database import get_session
from app.decorators.auth import jwt_authenticate
from app.models.auth import AuthUser
from app.encrypt.encrypt import encrypt_jwt, encrypt_sha
from app.response import response as resp


logger = logging.getLogger(__name__)

ns = api.namespace("auth", description="Endpoints for user auth")

parser = reqparse.RequestParser()
parser.add_argument("username", required=True)
parser.add_argument("password", required=True)



@ns.route("/login")
class Login(Resource):
    def post(self):
        try:
            parsed = parser.parse_args()
        except:
            return resp.error("username, password must be specified")
        
        # username and password check
        session = get_session("auth")
        auth_user = session.query(AuthUser).filter_by(username=parsed.username).first()
        if auth_user is None:
            return resp.error("Invalid username in token: {}".format(parsed.username))
        print (auth_user.password, encrypt_sha(parsed.password), parsed.password)
        if auth_user.password != encrypt_sha(parsed.password):
            return resp.error("Invalid password")

        # update last_login
        try:
            session.query(AuthUser).update({"last_login": datetime.now()})
            session.commit()
        except Exception as e:
            print (e)
            session.rollback()
            return resp.error("Error while update db", status=status.ERROR_SERVER)

        token = encrypt_jwt(parsed.username)
        return resp.success({
            "access_token": token
        })


@ns.route("/me")
class Me(Resource):
    @jwt_authenticate()
    def get(self, **kwargs):
        auth_user = kwargs["auth_user"]

        return resp.success({
            "id": auth_user.id,
            "username": auth_user.username,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "email": auth_user.email,
            "date_joined": auth_user.date_joined,
            "iat": kwargs["jwt_iat"],
            "exp": kwargs["jwt_exp"],
        })
        

@ns.route("/refresh")
class Refresh(Resource):
    @jwt_authenticate()
    def get(self, **kwargs):
        return resp.success({
            "access_token": encrypt_jwt(kwargs["jwt_username"])
        }) 
