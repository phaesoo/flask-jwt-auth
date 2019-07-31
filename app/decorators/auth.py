from flask import Flask, request
from functools import wraps
import jwt

from app.define import status
from app.response import response as resp

from app.db.database import get_session
from app.models.auth import AuthUser
from app.utils.config_util import get_config


def jwt_authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return resp.error("Token is not given")
        try:
            decoded_token = jwt.decode(token, get_config("JWT_SECRET_KEY"), algorithms=[get_config("JWT_ALGO")])
        except Exception as e:
            print e
            return resp.error("Invalid token given")

        session = get_session("auth")
        username = decoded_token.get("username")
        password = decoded_token.get("password")
        print username, "name"
        auth_user = session.query(AuthUser).filter_by(username="zz").first()
        if auth_user is None:
            return resp.error("Invalid username in token: {}".format(username))



        return f(*args, **kwargs)
    return decorated_function
            

        

        



