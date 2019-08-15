from flask import Flask, request
from functools import wraps
import jwt
import time

from app.define import status
from app.response import response as resp

from app.db.database import get_session
from app.encrypt.encrypt import decrypt_jwt, encrypt_sha
from app.models.auth import AuthUser
from app.utils.config_util import get_config


def jwt_authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return resp.error("Token is not given")
        try:
            decoded_token = decrypt_jwt(token)
        except Exception as e:
            print (e)
            return resp.error("Invalid token given")

        session = get_session("auth")
        username = decoded_token.get("aud")
        auth_user = session.query(AuthUser).filter_by(username=username).first()
        if auth_user is None:
            return resp.error("Invalid username in token: {}".format(username))
        
        if decoded_token.get("exp") < time.time():
            return resp.error("Access token has been expired", status=status.ERROR_UNAUTHORIZED)

        return f(*args, **kwargs)
    return decorated_function


def jwt_admin_authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token is None:
            return resp.error("Token is not given")
        try:
            decoded_token = decrypt_jwt(token)
        except Exception as e:
            print (e)
            return resp.error("Invalid token given")

        session = get_session("auth")
        username = decoded_token.get("username")
        auth_user = session.query(AuthUser).filter_by(username=username).first()
        if auth_user is None:
            return resp.error("Invalid username in token: {}".format(username))
        
        if decoded_token.get("exp") < time.time():
            return resp.error("Access token has been expired", status=status.ERROR_UNAUTHORIZED)

        if not auth_user.is_superuser:
            return resp.error("Admin only", status=status.ERROR_FORBIDDEN)

        return f(*args, **kwargs)
    return decorated_function


        



