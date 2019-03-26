import unittest
import json
from api.app import create_app
from database.db import DatabaseConnection
from api.utilitiez.auth_token import encode_token
from api.models.user import User
from api.models.message import Message


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

        self.message_data = {
            "subject": "My Andela Application",
            "message": "Joseph",
            "ParentMessageID": "121",
            "receiver": "kambugu"
        }

        self.user_id = 1
        self.token = encode_token(self.user_id)


        self.data = {}


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


    def test_create_message_subject_field_cannot_be_number(self):
        data = {
            "subject": "My Andela Application",
            "message": 3,
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


    def test_create_message_subject_field_length(self):
        data = {
            "subject": "My",
            "message": 3,
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


    def test_create_message_message_field_cannot_be_number(self):
        data = {
            "subject": 3,
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


    def test_duplicate_new_message(self):
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

    
    def test_duplicate_subject(self):
        message_data1 = {
            "subject": "My Andela Application",
            "message": "Jose",
            "ParentMessageID": "121",
            "receiver": "kambugu"
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(message_data1))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 409)
        self.assertEqual(response_data['status'], 409)
        self.assertIsInstance(response_data, dict)

    def test_duplicate_message_body(self):
        message_data1 = {
            "subject": "My Andela Application",
            "message": "Joseph",
            "ParentMessageID": "121",
            "receiver": "kambugu"
        }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(message_data1))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 409)
        self.assertEqual(response_data['status'], 409)
        self.assertIsInstance(response_data, dict)




    def test_get_message(self):
            self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
            res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
            self.assertEqual(res1.status_code, 200)
            self.client.post('/api/v1/messages', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
            res = self.client.get('/api/v1/messages/2', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
            response_data = json.loads(res.data.decode())
            self.assertEqual(response_data['status'], 404)
            self.assertEqual(res.status_code, 404)


    def test_get_message_with_no_token(self):
            self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
            res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
            self.assertEqual(res1.status_code, 200)
            self.client.post('/api/v1/messages', content_type="application/json",
                headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
            res = self.client.get('/api/v1/messages/2', content_type="application/json",
                data=json.dumps(self.message_data))
            response_data = json.loads(res.data.decode())
            self.assertEqual(response_data['status'], 401)
            self.assertEqual(res.status_code, 401)
           
    def test_get_message_not_existing(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.get('/api/v1/messages/3', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_delete_message(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.delete('/api/v1/messages/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)



    def test_delete_message_not_existing(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.delete('/api/v1/messages/3', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_get_all_sent(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.get('/api/v1/messages/sent', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_get_all_sent_empty_records(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v1/messages/sent', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_get_all_sent_mails_with_no_token(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            data=json.dumps(self.message_data))
        res = self.client.get('/api/v1/messages/sent', content_type="application/json",
            data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_get_all_received_emails(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        res = self.client.get('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_get_all_received_empty_inbox(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def tearDown(self):
        self.db.drop_table('users')
        self.db.drop_table('messages')
        