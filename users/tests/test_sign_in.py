import bcrypt
import json
import jwt
from unittest import mock

from django.test import TestCase, Client

from ..models import User
from ..service import SignInService
from my_settings import SECRET_KEY, ALGORITHM


class SignInViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        mock.patch.stopall()

    @mock.patch.object(User, 'get_by_user_email')
    def test_post_sign_in_success(self, get_by_user_email):
        get_by_user_email.return_value = User(
            email="test@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="myUser"
        )
        user_id = str(get_by_user_email.return_value.id)

        access_token = "Bearer " + jwt.encode({"id": user_id}, SECRET_KEY, ALGORITHM)
        data = {
            "email": "test@gmail.com",
            "password": "test123!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(),\
            {
                 "message": "SUCCESS",
                 "access_token": access_token
            })
        self.assertEqual(response.status_code, 200)

    def test_post_sign_in_key_error(self):
        data = {
            "키에러": "newUser@gmail.com",
            "password": "tset123@!"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    @mock.patch.object(SignInService, 'get_user')
    def test_post_sign_in_does_not_matched(self, get_user):
        get_user.return_value = User(
            email="newUser@gmail.com",
            password=bcrypt.hashpw(
                "test1234!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="myUser"
        )
        
        data = {
            "email": "oldUser@gmail.com",
            "password": "test123!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "INVALID_USER"})
        self.assertEqual(response.status_code, 404)
