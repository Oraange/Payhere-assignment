import bcrypt
import json
import jwt
from unittest import mock

from django.test import TestCase, Client

from users.service import SignInService
from account_books.models import AccountBook
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


class UpdateAccountBookViewTest(TestCase):
    
    @mock.patch.object(SignInService, 'get_user')
    def setUp(self, get_user):
        self.client = Client()
        get_user.return_value = User(
            email="test_update@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="testUser"
        )
        user_id = str(get_user.return_value.id)
        get_user.return_value.save()
        
        self.access_token = "Bearer " + jwt.encode({"id": user_id}, SECRET_KEY, ALGORITHM)

        self.book = AccountBook(
            type=AccountBook.Type.INCOME.value,
            amount=1000,
            category="역전우동",
            memo="뜨끈한 우동 한모금",
            user=get_user.return_value
        )
        self.book.save()

    def tearDown(self):
        mock.patch.stopall()

    def test_put_account_book_success(self):
        data = {
            "type" : 2,
            "amount" : 5000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.put(f'/account-books/{self.book.id}', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.status_code, 204)

    def test_put_account_book_does_not_exist(self):
        data = {
            "type" : 2,
            "amount" : 5000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.put('/account-books/10', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "ACCOUNT_BOOK_DOES_NOT_EXIST"})
        self.assertEqual(response.status_code, 404)

    @mock.patch.object(SignInService, 'get_user')
    def test_put_account_book_forbidden(self, get_user):
        get_user.return_value = User(
            email="test2@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="testUser2"
        )
        user_id = str(get_user.return_value.id)
        get_user.return_value.save()
        
        access_token = "Bearer " + jwt.encode({"id": user_id}, SECRET_KEY, ALGORITHM)
        data = {
            "type" : 2,
            "amount" : 5000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': access_token}
        response = self.client.put(f'/account-books/{self.book.id}', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "FORBIDDEN"})
        self.assertEqual(response.status_code, 403)

    def test_put_account_book_key_error(self):
        data = {
            "키에러" : 2,
            "amount" : 5000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.put(f'/account-books/{self.book.id}', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "KEY_ERROR"})
        self.assertEqual(response.status_code, 400)

    def test_put_account_book_value_error(self):
        data = {
            "type" : 2,
            "amount" : "5000",
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.put(f'/account-books/{self.book.id}', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "INVALID_VALUE"})
        self.assertEqual(response.status_code, 400)

    def test_put_account_book_type_not_1_or_2(self):
        data = {
            "type" : 50,
            "amount" : 5000,
            "category" : "편의점",
            "memo" : "삼각김밥"
        }
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.put(f'/account-books/{self.book.id}', json.dumps(data), content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "TYPE_MUST_BE_1_or_2"})
        self.assertEqual(response.status_code, 400)