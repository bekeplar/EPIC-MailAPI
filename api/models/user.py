"""FIle contains model for user"""
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

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



def is_valid_credentials(email, password):
    "checking for validity of user login details"
    for user in users:
        if user['email'] == email and check_password_hash(
                user['password'], password
        ):
            return user
    return None
