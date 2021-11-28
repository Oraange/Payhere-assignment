import bcrypt
import jwt

from users.exceptions import DuplicateUser, UserNotFound
from .dto import SignUpInputDTO
from .models import User
from my_settings import SECRET_KEY, ALGORITHM


class SignUpService:
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
        if User.get_by_user_email(sign_up_info.email):
            raise DuplicateUser

        return User.add(new_user)
        

class SignInService:
    def get_user(self, email):
        user = User.get_by_user_email(email)
        if not user:
            raise UserNotFound
        
        return user

    def check_password(self, plain_password, hashed_password):
        if not bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8")):
            raise UserNotFound


class TokenGenerator:
    def __init__(self):
        self.sign_in_service = SignInService()

    def generate_token(self, user_id):
        return {"access_token": "Bearer " + jwt.encode({"id": str(user_id)}, SECRET_KEY, ALGORITHM)}
