"""FIle contains model for user"""
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    """Class to contain all user objects"""

    def __init__(self, **kwargs):
        self.user_id = kwargs["user_id"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.email = kwargs["email"]
        self.password = generate_password_hash(kwargs["password"])
        self.registered_on = date.today()
        self.is_admin = False
    