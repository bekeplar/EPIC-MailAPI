from tests.base import BaseTest
import json


class UserTestCase(BaseTest):
    def test_home_page(self):
        """unit test for success to index endpoint"""
        response = self.client.get("/", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data).get("message"), "Welcome to Epic-Email App")


    def test_method_not_allowed(self):
        """unit test for method not allowed error"""
        response = self.client.patch('/', data=json.dumps({
            "username": "username",
            "password": "password"
        }), content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response_data.get("error"), "Method not allowed")


    def test_page_not_found(self):
        """unit test for page not found error"""
        response = self.client.get(
            "url/not/exist", content_type="application/json")
        response_data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_data.get("error"), "Endpoint for specified URL does not exist")

    def test_can_signup_user(self):
        
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)

    def test_can_signup_user_with_no_data(self):  
        res = self.client.post('/api/v2/auth/signup', content_type="application/json")
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_first_name_is_not_a_string(self):
        data = {
                "firstname": 2222,
                "lastname": "Joseph",
                "email": "bekeplar@gmail.com",
                "password": "Bekeplar1234"
                }
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
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
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
        
    def test_returns_error_if_user_already_exists(self):
                
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res = self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,409)
        self.assertEqual(response_data['status'], 409)
        self.assertIsInstance(response_data, dict)

    def test_can_login_user(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))
        res = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_can_login_with_no_data(self):
        data = {
            "firstname": "Bekalaze",
            "lastname": "Joseph",
            "email": "bekeplar@gmail.com",
            "password": "Bekeplar1234"
                }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(data))
        res = self.client.post('/api/v2/auth/login', content_type="application/json")
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)
       
       
    def test_returns_error_on_invalid_login_details(self):
        login_data = {
                       "email":"bekeplar@gmail.com",
                       "password": "Bekeplax233"
                     }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))
        res = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)

    def test_returns_error_if_missing_key(self):
        login_data = {
                       "email":"bekeplar@gmail.com"
                
                    }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))
        res = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(login_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code,422)
        self.assertEqual(response_data['status'], 422)
        self.assertIsInstance(response_data, dict)

        
        