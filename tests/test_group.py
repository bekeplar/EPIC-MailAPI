from tests.base import BaseTest
import json

class MessageTestCase(BaseTest):

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


    def test_delete_group(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.delete('/api/v1/groups/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_delete_existing_not_existing(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.delete('/api/v1/groups/100', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_get_all_groups(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.get('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_get_all_groups_empty_list(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)

    def test_get_all_groups_with_no_token(self):
        self.client.post('/api/v1/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v1/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v1/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.get('/api/v1/groups', content_type="application/json",
            data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    

