import unittest
import json
from api.app import create_app
from database.db import DatabaseConnection
from api.utilitiez.auth_token import encode_token
from api.models.user import User
from api.models.group import Group


class MessageTestCase(unittest.TestCase):

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

        self.group_data = {
            "group_name": "Andela21",
        }

        self.user_id = 1
        self.token = encode_token(self.user_id)
        self.data = {}


    def test_create_new_group(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)


    def test_create_group_without_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_group_name_is_empty_string(self):
        data = {
            "group_name": ""
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_group_name_is_not_string(self):
        data = {
            "group_name": 222
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def tearDown(self):
        self.db.drop_table('users')
        self.db.drop_table('groups')

