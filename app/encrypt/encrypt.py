from flask import current_app as app

import jwt
from hashlib import sha256
from datetime import datetime
from app.utils.config_util import get_config


# aud: audience
# iat: issued at
# exp: expiration time


def __validate_jwt(data):
    for key in ["aud", "iat", "exp"]:
        if key not in data:
            raise KeyError


def encrypt_jwt(aud):
    iat = int(datetime.now().timestamp())
    exp = iat + get_config("JWT_EXP_PERIOD")
    return jwt.encode({
        "aud": aud, 
        "iat": iat,
        "exp": exp
    }, get_config("JWT_SECRET_KEY"), algorithm=get_config("JWT_ALGO"))


def decrypt_jwt(token):
    data = jwt.decode(token, get_config("JWT_SECRET_KEY"), algorithms=[get_config("JWT_ALGO")])
    __validate_jwt(data)
    return data


def encrypt_sha(hash_string):
    return sha256(hash_string.encode()).hexdigest()
