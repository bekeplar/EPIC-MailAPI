import unittest
import json
from api.app import create_app
from api.views import user
from api.models.user import User, users


class UserTestCase(unittest.TestCase):

    def setUp(self):
        """initializing method for a unit test"""
        self.app = create_app("Testing")
        self.client = self.app.test_client(self)
        
        self.data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "bekeplax@gmail.com",
                "password": "Bekeplar1234"
                }

    
    def test_can_signup_user(self):
        
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)

    def test_can_signup_user_with_no_data(self):
        
        res = self.client.post('/api/v1/auth/signup', content_type="application/json")
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
            
    def test_register_with_missing_fields(self):
        data = {
                "firstname": "",
                "lastname": "",
                "email": "",
                "password": ""
            }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        



    def test_returns_error_if_email_is_missing(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "",
                "password": "Bekeplar1234"
        }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        
    
    def test_returns_error_if_first_name_not_string(self):
        data = {
                "firstname": 123,
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        

    def test_missing_first_name(self):
        data = {
                "firstname": "",
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        

    def test_missing_last_name(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        
    def test_last_name_is_not_a_string(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": 2233,
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_email_validity(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "bekeplargmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        

    def test_validity_of_password(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        
    def test_password_strength(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bek12"
                }
        res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        
    # def test_returns_error_if_user_already_exists(self):
                
    #     self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.data))        
    #     res = self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.data))
    #     response_data = json.loads(res.data.decode())
    #     self.assertEqual(res.status_code,409)
    #     self.assertEqual(response_data['status'], 409)
    #     self.assertIsInstance(response_data, dict)

    def test_can_login_user(self):
        data = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "email": "bekeplar@gmail.com",
            "password": "Bekeplar1234"
                }
        login_data = {
                       "email":"bekeplar@gmail.com",
                       "password": "Bekeplar1234"
                     }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        res = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)
       
       
    def test_returns_error_on_invalid_login_details(self):
        data = {
                "firstname": "Bekalaze",
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        login_data = {
                       "email":"bekeplar@gmail.com",
                       "password": "Bekeplax233"
                     }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        res = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_returns_error_if_missing_key(self):
        data = {
                "firstname": "Bekalaze",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
            }

        login_data = {
                       "email":"bekeplar@gmail.com"
                
                    }
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(data))
        res = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,422)
        self.assertEqual(response_data['status'], 422)
        self.assertIsInstance(response_data, dict)


   
    def tearDown(self):
            pass
        