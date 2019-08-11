from flask_restplus import Resource, reqparse
import logging
from datetime import datetime

from app.api.restplus import api
from app.define import status
from app.db.database import get_session
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
            parse_data = parser.parse_args()
        except:
            return resp.error("username, password must be specified")
        
        # username and password check
        session = get_session("auth")
        auth_user = session.query(AuthUser).filter_by(username=parse_data.username).first()
        if auth_user is None:
            return resp.error("Invalid username in token: {}".format(parse_data.username))
        if auth_user.password != encrypt_sha(parse_data.password):
            return resp.error("Invalid password")

        # update last_login
        try:
            session.query(AuthUser).update({"last_login": datetime.now()})
            session.commit()
        except Exception as e:
            print (e)
            session.rollback()
            return resp.error("Error while update db", status=status.ERROR_SERVER)

        token = encrypt_jwt(aud=parse_data.username)
        return resp.success({
            "access_token": token
        })
