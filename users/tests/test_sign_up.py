import json
from unittest import mock

from django.test import TestCase, Client

from ..models import User


class SignUpViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        mock.patch.stopall()

    def test_post_sign_up_success(self):
        data = {
            "email": "newUser@gmail.com",
            "password": "test123!@",
            "nick_name": "newUser"
        }
        response = self.client.post('/users/sign-up', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "CREATED"})
        self.assertEqual(response.status_code, 201)

    def test_post_sign_up_key_error(self):
        data = {
            "키에러": "newUser@gmail.com",
            "password": "tset123@!",
            "nick_name": "newUser"
        }
        response = self.client.post('/users/sign-up', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    @mock.patch.object(User, 'get_by_user_email')
    def test_post_sign_up_duplicate_error(self, get_by_user_email):
        get_by_user_email.return_value = User(
            email="newUser@gmail.com",
            password="testtest123!",
            nick_name="myUser"
        )
        
        data = {
            "email": "newUser@gmail.com",
            "password": "tset123!@",
            "nick_name": "newUser"
        }
        response = self.client.post('/users/sign-up', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "USER_ALREADY_EXIST"})
        self.assertEqual(response.status_code, 409)

    def test_post_sign_up_invalid_email(self):
        data = {
            "email": "hello",
            "password": "test123@!",
            "nick_name": "newUser"
        }
        response = self.client.post('/users/sign-up', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "INVALID_EMAIL"})
        self.assertEqual(response.status_code, 400)

    def test_post_sign_up_invalid_password(self):
        data = {
            "email": "abc@gmail.com",
            "password": "1234",
            "nick_name": "newUser"
        }
        response = self.client.post('/users/sign-up', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "INVALID_PASSWORD"})
        self.assertEqual(response.status_code, 400)
        