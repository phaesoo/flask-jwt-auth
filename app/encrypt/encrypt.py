from flask import current_app as app
import jwt

from app.utils.config_util import get_config


def __validate(data):
    for key in ["username", "password"]:
        if key not in data:
            raise KeyError

def encode(username, password, **kwargs):
    return jwt.encode({
        "username": username, 
        "password": password
    }, get_config("JWT_SECRET_KEY"), algorithm=get_config("JWT_ALGO"))


def decode(token):
    data = jwt.decode(token, get_config("JWT_SECRET_KEY"), algorithms=[get_config("JWT_ALGO")])
    __validate(data)
    return data