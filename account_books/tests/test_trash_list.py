import jwt
from unittest.mock import patch

from django.test import TestCase, Client

from account_books.models import AccountBook
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


class TrashedBookListViewTest(TestCase):
    @patch.object(AccountBook, 'get_queryset_by_user')
    @patch.object(User, 'get_by_id')
    def setUp(self, get_user, get_qs):
        self.client = Client()

        get_user.return_value = User(
            email="test1@test.com",
            password="test1234!@",
            nick_name="test_1"
        )
        user_1 = get_user.return_value
        user_1.save()
        self.access_token = "Bearer " + jwt.encode({"id": str(user_1.id)}, SECRET_KEY, ALGORITHM)
        user_2 = User(
            email="test2@test.com",
            password="test1234!@",
            nick_name="test_2"
        )
        user_2.save()
        self.access_token_2 = "Bearer " + jwt.encode({"id": str(user_2.id)}, SECRET_KEY, ALGORITHM)

        book_1 = AccountBook(
            id=1,
            type=2,
            amount=1000,
            category="편의점",
            memo="맛있는 삼각김밥",
            user=user_1,
            is_deleted=True
        )
        book_1.save()
        book_2 = AccountBook(
            id=2,
            type=2,
            amount=3500,
            category="중국집",
            memo="손짜장",
            user=user_1,
            is_deleted=True
        )
        book_2.save()
        book_3 = AccountBook(
            id=3,
            type=2,
            amount=500,
            category="편의점",
            memo="사탕",
            user=user_1,
            is_deleted=True
        )
        book_3.save()
        get_qs.return_value = AccountBook.objects.filter(id__in=[1,2,3])
        self.qs = get_qs.return_value.order_by('-updated_at')

        session = self.client.session
        session["user"]=str(user_1.id)
        session.save()

    def tearDown(self):
        patch.stopall()

    def test_get_trash_book_list_success(self):
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.get('/account-books/trash', content_type="application/json", **header)
        self.maxDiff = None
        self.assertEqual(response.json(),\
            {
                "total_count": 3,
                "results": [
                    {
                        "id": book.id,
                        "updated_at": book.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "type": "income" if book.type==1 else "outlay",
                        "amount": book.amount,
                        "category": book.category,
                        "memo": book.memo
                    } for book in self.qs]
            })
        self.assertEqual(response.status_code, 200)

    def test_get_trash_book_list_not_found(self):
        header = {'HTTP_Authorization': self.access_token_2}
        response = self.client.get('/account-books/trash', content_type="application/json", **header)
        self.assertEqual(response.json(),{"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"})
        self.assertEqual(response.status_code, 404)

    def test_get_trash_book_invalid_params(self):
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.get('/account-books/trash?offset=0&limit=a', content_type="application/json", **header)
        self.assertEqual(response.json(),{"message": "PARAMETER_ERROR"})
        self.assertEqual(response.status_code, 400)