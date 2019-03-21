"""File for all user authentication code"""
import datetime
from functools import wraps
from os import environ

import jwt
from flask import request, jsonify

from api.utilitiez.responses import (
    expired_token_message,
    invalid_token_message
    )

secret_key = environ.get("SECRET_KEY", "let-me-add-mine")


def encode_token(user_id, isAdmin=False):
    payload = {
        "userid": user_id,
        "isAdmin": isAdmin,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")

    return token


def decode_token(token):
    decoded = jwt.decode(str(token), secret_key, algorithm="HS256")
    return decoded






