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


def encode_token(user_id, is_Admin=False):
    payload = {
        "userid": user_id,
        "isAdmin": is_Admin,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3),
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")

    return token


def decode_token(token):
    decoded = jwt.decode(str(token), secret_key, algorithm="HS256")
    return decoded


def extract_token_from_header():
    authorizaton_header = request.headers.get("Authorization")
    if not authorizaton_header or "Bearer" not in authorizaton_header:
        return (
            jsonify({"error": "Bad authorization header", "status": 400}),
            400,
        )
    token = str(authorizaton_header).split(" ")[1]
    return token


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            token = extract_token_from_header()
            decode_token(token)
            response = func(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            response = (
                jsonify({"error": expired_token_message, "status": 401}),
                401,
            )
        except jwt.InvalidTokenError:
            response = (
                jsonify({"error": invalid_token_message, "status": 401}),
                401,
            )
        return response

    return wrapper


def get_current_identity():
    return decode_token(extract_token_from_header())["userid"]


