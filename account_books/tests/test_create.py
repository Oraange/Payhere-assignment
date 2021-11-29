import json
import jwt
from unittest.mock import patch

from django.test import TestCase, Client

from users.models import User
from my_settings import SECRET_KEY, ALGORITHM

class CreateAccountBookViewTest(TestCase):
    @patch.object(User, 'get_by_id')
    def setUp(self, get_user):
        self.client = Client()
    
        get_user.return_value = user_1 = User(
            email="test@gmail.com",
            password="test123!@",
            nick_name="test_user_1"
        )
        get_user.return_value.save()

        self.access_token = "Bearer " + jwt.encode({"id": str(user_1.id)}, SECRET_KEY, ALGORITHM)


    def tearDown(self):
        User.objects.all().delete()

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
        self.assertEqual(response.json(), {"message": "INVALID_KEY"})
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
        self.assertEqual(response.json(), {"message": "INVALID_VALUE"})
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