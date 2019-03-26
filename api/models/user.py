"""FIle contains model for user"""

from werkzeug.security import generate_password_hash, check_password_hash

from api.utilitiez.responses import (
    duplicate_email,
)
from database.db import DatabaseConnection
class User:
    """Class to contain all user objects"""

    def __init__(self, **kwargs):
        # Generating a user's database fr string user objects
        self.db = DatabaseConnection()

    def insert_user(self, **kwargs):
        """User class method for adding new user to the users database"""
        first_name = kwargs["first_name"]
        last_name = kwargs["last_name"]
        email = kwargs["email"]
        user_password = generate_password_hash(kwargs["password"])

        # Querry for adding a new user into users_db
        sql = (
            "INSERT INTO users ("
            "first_name,"
            "last_name, "
            "email,"
            "user_password )VALUES ("
            f"'{first_name}', '{last_name}','{email}',"
            f"'{user_password}') returning "
            "user_id, first_name as firstname,"
            "last_name as lastname,"
            "email as email"
        )
        self.db.cursor_database.execute(sql)
        new_user = self.db.cursor_database.fetchone()
        return new_user

    def check_if_user_exists(self, email):
        """Making sure that a user's email is unique"""
        user_exists_sql = (
            "SELECT email from users where "
            f" email='{email}';"
        )
        self.db.cursor_database.execute(user_exists_sql)
        user_exists = self.db.cursor_database.fetchone()
        error = {}

        if user_exists and user_exists.get("email") == email:
            error["email"] = duplicate_email

        return error

    def is_valid_credentials(self, email, user_password):
        """Function for verrifying user credentials before login"""
        sql = (
            "SELECT user_id, email ,user_password FROM users \
                where email="
            f"'{email}';"
        )
        self.db.cursor_database.execute(sql)

        user_details = self.db.cursor_database.fetchone()

        if (
                user_details
                and user_details.get("email") == email
                and check_password_hash(
                user_details.get("user_password"), user_password
        )
        ):
            id = user_details.get("user_id")

            return id
        return None
    
    