import bcrypt
import json
import jwt
from unittest import mock

from django.test import TestCase, Client

from users.service import SignInService
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

class CreateAccountBookViewTest(TestCase):

    @mock.patch.object(SignInService, 'get_user')
    def setUp(self, get_user):
        self.client = Client()
        get_user.return_value = User(
            email="test@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="testUser"
        )
        user_id = str(get_user.return_value.id)
        get_user.return_value.save()

        self.access_token = "Bearer " + jwt.encode({"id": user_id}, SECRET_KEY, ALGORITHM)


    def tearDown(self):
        mock.patch.stopall()

    def test_post_account_book_success(self):
        data = {
            "type" : 1,
            "amount" : 1000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/account-books', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "CREATED"})
        self.assertEqual(response.status_code, 201)

    def test_post_account_book_key_error(self):
        data = {
            "키에러" : 1,
            "amount" : 1000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/account-books', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_post_account_book_type_not_1_or2(self):
        data = {
            "type" : 3,
            "amount" : 1000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/account-books', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "TYPE_MUST_BE_1_or_2"})
        self.assertEqual(response.status_code, 400)

    def test_post_account_book_value_error(self):
        data = {
            "type" : 1,
            "amount" : "2000",
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/account-books', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "INVALID_VALUE"})
        self.assertEqual(response.status_code, 400)