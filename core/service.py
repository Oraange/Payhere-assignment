from users.models import User
from .exceptions import UserNotFound


class Authentication:
    def get_user(self, user_id):
        user = User.get_by_user_id(user_id)
        if not user:
            raise UserNotFound

        return user