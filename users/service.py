import bcrypt

from users.exceptions import DuplicateUser, UserNotFound
from .dto import SignUpInputDTO
from .models import User


class UserService:
    def get_user(self, email):
        user = User.get_by_user_email(email)

        if not user:
            raise UserNotFound
        
        else:
            return user

    def encrypte_password(self, plain_password):
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
        decode_password = hashed_password.decode("utf-8")

        return decode_password

    def add_user(self, sign_up_info: SignUpInputDTO):

        new_user = User(
            email=sign_up_info.email,
            password=self.encrypte_password(sign_up_info.password),
            nick_name=sign_up_info.nick_name
        )

        try:
            return User.add(new_user)
        
        except Exception:
            return DuplicateUser
