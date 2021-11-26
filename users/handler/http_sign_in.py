import json

from django.views import View
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class SignInInputDTO:
    email: str
    password: str


class SignInOutputDTO:
    access_token: str


class SignInHandler(View):
    def __init__(self, request):
        self.data = json.loads(request.body)

    def sign_in_request(self):
        try:
            validate_email(self.data["email"])

        except ValidationError:
            return {"message": "INVALID_EMAIL"}

        else:    
            SignInInputDTO.email = self.data["email"]
            SignInInputDTO.password = self.data["password"]

            return SignInInputDTO()
