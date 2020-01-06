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

def jwt_authenticate(is_superuser=False):
    def _jwt_authenticate(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token is None:
                return resp.error("Token is not given", status=status.ERROR_UNAUTHORIZED)
            try:
                decoded_token = decrypt_jwt(token)
            except Exception as e:
                print (e)
                return resp.error("Invalid token given", status=status.ERROR_UNAUTHORIZED)

            session = get_session("auth")
            username = decoded_token["username"]

            auth_user = session.query(AuthUser).filter_by(username=username).first()
            if auth_user is None:
                return resp.error("Invalid username in token: {}".format(username), status=status.ERROR_UNAUTHORIZED)
            
            exp = decoded_token["exp"]
            if exp < time.time():
                return resp.error("Access token has been expired", status=status.ERROR_UNAUTHORIZED)

            if is_superuser and not auth_user.is_superuser:
                return resp.error("Admin only", status=status.ERROR_FORBIDDEN)

            kwargs["jwt_username"] = username
            kwargs["jwt_exp"] = exp
            kwargs["jwt_iat"] = decoded_token["iat"]
            kwargs["auth_user"] = auth_user

            return f(*args, **kwargs)
        return decorated_function
    return _jwt_authenticate