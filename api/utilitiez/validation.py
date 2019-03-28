"""Module contains functions for validating user inputs as provided"""
import re
from flask import jsonify, request
from functools import wraps
from api.utilitiez.responses import (
    wrong_password,
    wrong_name,
    wrong_email,
    invalid_id,
    
)


def sign_up_data_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        if not request.data:

            response = (
                jsonify(
                    {
                        "error": "Provide provide valid data to register",
                        "status": 400,
                    }
                ),
                400,
            )
        else:
            response = func(*args, **kwargs)
        return response

    return wrapper


def is_number(num_value):
    """Checks if num_value is a number"""
    if isinstance(num_value, int) or isinstance(num_value, float):
        return True
    return False


def is_string(str_value):
    """Checks if input is a string"""
    if (
            str_value
            and isinstance(str_value, str)
            and not str(str_value).isspace()
            and not str_value.isnumeric()
    ):
        return True
    return False


def contains_space(str_value):
    """Checks if input contains a space"""
    if " " in str_value or len(str(str_value).split(" ")) > 1:
        return True
    return False


def contains_number(str_value):
    """Checks if input contains a space"""
    for character in str_value:
        if character.isdigit():
            return True
    return False


def validate_email(email):
    if not email or not re.match("[^@]+@[^@]+\.[^@]+", email):
        return wrong_email
    return None


def validate_name(name, required=1):
    error = wrong_name
    if not required and len(str(name).strip()) == 0:
        error = None
    elif (
            name
            and is_string(name)
            and not contains_space(name)
            and not contains_number(name)
    ):
        error = None
    return error


def validate_password(password):
    error = wrong_password
    if (
            len(password) >= 8
            and re.search("[A-Z]", password)
            and re.search("[0-9]", password)
            and re.search("[a-z]", password)
    ):
        error = None
    return error


def validate_new_user(**kwargs):
    errors = dict()
    errors["firstname"] = validate_name(kwargs["first_name"])
    errors["lastname"] = validate_name(kwargs["last_name"])
    errors["password"] = validate_password(kwargs["password"])
    errors["email"] = validate_email(kwargs["email"])
    invalid_fields = {key: value for key, value in errors.items() if value}
    if invalid_fields:
        return jsonify({"status": 400, "error": invalid_fields}), 400
    return None


def validate_sentence(sentence, min_len=0, max_len=0):
    error = None
    sentence = str(sentence).strip()
    if sentence.isdigit():
        error = "Field cannot be a number"
    elif len(sentence) < min_len:
        error = f"Field must contain a minimum of {str(min_len)} characters"
    elif max_len and len(sentence) > max_len:
        error = f"Field must contain a maximum of {str(max_len)} characters"

    return error


def validate_new_message(**kwargs):
    errors = dict()
    errors["subject"] = validate_sentence(kwargs.get("subject"), 10)
    errors["message"] = validate_sentence(kwargs.get("message"), 4, 100)
    not_valid = {key: value for key, value in errors.items() if value}
    if not_valid:
        return (jsonify({"status": 400, "error": not_valid}), 400)
    return None


def validate_group(**kwargs):
    errors = dict()
    errors["group_name"] = validate_sentence(kwargs.get("group_name"),4, 100)
    not_valid = {key: value for key, value in errors.items() if value}
    if not_valid:
        return (jsonify({"status": 400, "error": not_valid}), 400)
    return None


