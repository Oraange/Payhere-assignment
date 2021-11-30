import jwt
from unittest.mock import patch

from django.test import TestCase, Client

from account_books.models import AccountBook
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


class AccountBookDetailViewTest(TestCase):
    @patch.object(AccountBook, 'get_by_id')
    @patch.object(User, 'get_by_id')
    def setUp(self, get_user, get_book):
        self.client = Client()

        get_user.return_value = User(
            email="test1@test.com",
            password="test1234!@",
            nick_name="test_1"
        )
        user_1 = get_user.return_value
        user_1.save()
        self.access_token_1 = "Bearer " + jwt.encode({"id": str(user_1.id)}, SECRET_KEY, ALGORITHM)
        user_2 = User(
            email="test2@test.com",
            password="test1234!@",
            nick_name="test_2"
        )
        user_2.save()
        self.access_token_2 = "Bearer " + jwt.encode({"id": str(user_2.id)}, SECRET_KEY, ALGORITHM)

        self.book_1 = AccountBook(
            id=1,
            type=2,
            amount=1000,
            category="편의점",
            memo="맛있는 삼각김밥",
            user=user_1
        )
        self.book_1.save()
        book_2 = AccountBook(
            id=2,
            type=2,
            amount=3500,
            category="중국집",
            memo="손짜장",
            user=user_1
        )
        book_2.save()
        
        get_book.return_value = self.book_1

        session = self.client.session
        session["user"]=str(user_1.id)
        session.save()

    def tearDown(self):
        patch.stopall()

    def test_get_account_book_success(self):
        header = {'HTTP_Authorization': self.access_token_1}
        response = self.client.get('/account-books/1', content_type="application/json", **header)
        self.maxDiff = None
        self.assertEqual(response.json(),\
            {
                "id": self.book_1.id,
                "updated_at": self.book_1.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                "type": "income" if self.book_1.type==1 else "outlay",
                "amount": self.book_1.amount,
                "category": self.book_1.category,
                "memo": self.book_1.memo
            })
        self.assertEqual(response.status_code, 200)

    def test_get_account_book_not_found(self):
        header = {'HTTP_Authorization': self.access_token_1}
        response = self.client.get('/account-books/10', content_type="application/json", **header)
        self.assertEqual(response.json(),{"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"})
        self.assertEqual(response.status_code, 404)

    def test_get_account_book_forbidden(self):
        header = {'HTTP_Authorization': self.access_token_2}
        response = self.client.get('/account-books/1', content_type="application/json", **header)
        self.assertEqual(response.json(),{"message": "FORBIDDEN"})
        self.assertEqual(response.status_code, 403)
