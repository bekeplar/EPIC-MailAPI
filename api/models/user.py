"""FIle contains model for user"""
from datetime import date
from api.utilitiez.auth_token import get_current_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.utilitiez.responses import (
    duplicate_email,
    duplicate_first_name,
    duplicate_last_name,
)
users = []
user_id = 1


class User:
    """class to contain all user objects"""

    def __init__(self, **kwargs):
        global user_id
        self.user_id = user_id
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.email = kwargs["email"]
        self.password = generate_password_hash(kwargs["password"])
        self.registered_on = date.today()
        self.is_admin = False
        user_id += 1


def check_user_exists(first_name, last_name, email):
    """Testing for duplication of user_details"""
    for user in users:
        if user.email == email:
            return duplicate_email
        elif user.first_name == first_name:
            return duplicate_first_name
        elif user.last_name == last_name:
            return duplicate_last_name

