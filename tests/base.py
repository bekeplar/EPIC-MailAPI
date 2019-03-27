import unittest
import json
from api.app import create_app
from database.db import DatabaseConnection
from database.db import DatabaseConnection
from api.utilitiez.auth_token import encode_token
from api.models.user import User
from api.models.group import Group
from api.models.message import Message


class BaseTest(unittest.TestCase):

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        self.db = DatabaseConnection()


        self.user_data = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "email": "bekeplar@gmail.com",
            "password": "Bekeplar1234"
                }

        self.user_login_data = {
            "email":"bekeplar@gmail.com",
            "password": "Bekeplar1234"
            }

        self.message_data = {
            "subject": "My Andela Application",
            "message": "Joseph",
            "ParentMessageID": "121",
            "receiver": "kambugu"
        }


        self.group_data = {
            "group_name": "Andela21",
        }

        self.user_id = 1
        self.token = encode_token(self.user_id)
        self.data = {}

    def tearDown(self):
        self.db.drop_table('users')
        self.db.drop_table('messages')
        self.db.drop_table('groups')

if __name__ == "__main__":
    unittest.main()


