import bcrypt
import json
import jwt
from unittest import mock

from django.test import TestCase, Client

from ..models import User
from ..service import SignInService
from my_settings import SECRET_KEY, ALGORITHM


class SignInViewTest(TestCase):
    @mock.patch.object(SignInService, 'get_user')
    def setUp(self, get_user):
        self.client = Client()

        get_user.return_value = User(
            email="test@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="myUser"
        )
        user_id = str(get_user.return_value.id)
        get_user.return_value.save()

        self.access_token = "Bearer " + jwt.encode({"id": user_id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        mock.patch.stopall()

    def test_post_sign_in_success(self):
        data = {
            "email": "test@gmail.com",
            "password": "test123!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(),\
            {
                 "message": "SUCCESS",
                 "access_token": self.access_token
            })
        self.assertEqual(response.status_code, 200)

    def test_post_sign_in_key_error(self):
        data = {
            "키에러": "test@gmail.com",
            "password": "test123!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_post_sign_in_does_not_matched_email(self):
        data = {
            "email": "oldUser@gmail.com",
            "password": "test123!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "INVALID_USER"})
        self.assertEqual(response.status_code, 404)

    def test_post_sign_in_does_not_matched_password(self):
        data = {
            "email": "test@gmail.com",
            "password": "test1234!@"
        }
        response = self.client.post('/users/sign-in', json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), {"message": "INVALID_USER"})
        self.assertEqual(response.status_code, 404)
