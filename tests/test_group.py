from tests.base import BaseTest
import json

class MessageTestCase(BaseTest):

    def test_create_new_group(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)


    def test_create_group_without_data(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_group_name_is_empty_string(self):
        data = {
            "group_name": ""
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_group_name_is_not_string(self):
        data = {
            "group_name": 222
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_delete_group(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.delete('/api/v2/groups/1', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_delete_group_not_existing(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.delete('/api/v2/groups/100', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_get_all_groups(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.get('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_get_all_groups_empty_list(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.get('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)

    def test_get_all_groups_with_no_token(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.get('/api/v2/groups', content_type="application/json",
            data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_edit_group_name(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.patch('/api/v2/groups/1/name', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data1))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_data['status'], 200)
        self.assertIsInstance(response_data, dict)


    def test_edit_group_name_not_present(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.patch('/api/v2/groups/4/name', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data1))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)


    def test_edit_group_name_no_token(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.patch('/api/v2/groups/1/name', content_type="application/json",
            data=json.dumps(self.group_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)


    def test_add_member_without_data(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/users', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_delete_member_not_existing(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        self.client.post('/api/v2/groups', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_data))
        res = self.client.delete('/api/v2/groups/1/users/7', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.member))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 404)
        self.assertEqual(response_data['status'], 404)
        self.assertIsInstance(response_data, dict)

    def test_create_message(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(self.group_message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 201)
        self.assertEqual(response_data['status'], 201)
        self.assertIsInstance(response_data, dict)


    def test_create_message_without_data(self):
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token})
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_empty_subject(self):
        data = {
            "subject": "",
            "message": "Joseph",
            "ParentMessageID": "121",
            "groupId": "1" 
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_empty_message(self):
        data = {
            "subject": "My Andela Application",
            "message": "",
            "ParentMessageID": "121",
            "groupId": "1"
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_missing_subject_field(self):
        data = {
            "message": "Joseph",
            "ParentMessageID": "121",
            "groupId": "1" 
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)

    def test_create_message_subject_field_cannot_be_number(self):
        data = {
            "subject": "My Andela Application",
            "message": 3,
            "ParentMessageID": "121",
            "groupId": "1"
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_message_subject_field_length(self):
        data = {
            "subject": "My",
            "message": 3,
            "ParentMessageID": "121",
            "groupId": "1" 
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_message_message_field_cannot_be_number(self):
        data = {
            "subject": 3,
            "message": "Joseph",
            "ParentMessageID": "121",
            "groupId": "1" 
        }
        self.client.post('/api/v2/auth/signup', content_type="application/json", data=json.dumps(self.user_data))        
        res1 = self.client.post('/api/v2/auth/login', content_type="application/json", data=json.dumps(self.user_login_data))
        self.assertEqual(res1.status_code, 200)
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            headers={'Authorization': 'Bearer ' + self.token}, data=json.dumps(data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 400)
        self.assertEqual(response_data['status'], 400)
        self.assertIsInstance(response_data, dict)


    def test_create_message_without_token(self):
        res = self.client.post('/api/v2/groups/1/messages', content_type="application/json",
            data=json.dumps(self.message_data))
        response_data = json.loads(res.data.decode())
        self.assertEqual(res.status_code, 401)
        self.assertEqual(response_data['status'], 401)
        self.assertIsInstance(response_data, dict)








        
    



    

