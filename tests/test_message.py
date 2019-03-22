import unittest
import json
from api.app import create_app
from api.views import user
from api.models.message import Message, user_messages
from api.models.user import User, users
from api.utilitiez.auth_token import encode_token


class MessageTestCase(unittest.TestCase):

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        
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

        self.user_id = 1
        self.token = encode_token(self.user_id)


        self.data = {}


    def tearDown(self):
        users.clear()
        user_messages.clear()


    def test_create_message(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)

    def test_create_message_without_data(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_message_empty_subject(self):
        data = {
            "subject": "",
            "message": "Joseph",
            "ParentMessageID": "121" 
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_empty_message(self):
        data = {
            "subject": "My Andela Application",
            "message": "",
            "ParentMessageID": "121" 
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_missing_subject_field(self):
        data = {
            "message": "Joseph",
            "ParentMessageID": "121" 
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_without_token(self):
        res = self.client.post('/api/v1/messages', content_type="application/json",
            data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_duplicate_message(self):
            self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
            res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
            self.assertEqual(res1.status_code, 200)
            self.client.post('/api/v1/messages', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
            res = self.client.post('/api/v1/messages', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
            response_data = json.loads(res.data.decode())
            self.assertEqual(res.status_code, 409)
            self.assertEqual(response_data['status'], 409)
            self.assertIsInstance(response_data, dict)


