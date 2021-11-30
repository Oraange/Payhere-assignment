import bcrypt
import jwt
from unittest.mock import patch

from django.test import TestCase, Client

from ..models import User
from my_settings import SECRET_KEY, ALGORITHM


class LogOutViewTest(TestCase):
    @patch.object(User, 'get_by_email')
    def setUp(self, get_user):
        self.client = Client()

        get_user.return_value = User(
            email="test@gmail.com",
            password=bcrypt.hashpw(
                "test123!@".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8"),
            nick_name="myUser"
        )
        self.user_1 = get_user.return_value
        self.user_1.save()

        self.access_token = "Bearer " + jwt.encode({"id": str(self.user_1.id)}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        patch.stopall()

    def test_post_log_out_success(self):
        session = self.client.session
        session["user"]=str(self.user_1.id)
        session.save()

        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/users/log-out', content_type="text/html", **header)
        self.assertEqual(response.status_code, 302)

    def test_post_log_in_required(self):
        header = {'HTTP_Authorization': self.access_token}
        response = self.client.post('/users/log-out', content_type="application/json", **header)
        self.assertEqual(response.json(), {"message": "SESSION_EXPIRED"})
        self.assertEqual(response.status_code, 401)
