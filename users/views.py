import json

from django.http import JsonResponse
from django.views import View
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from users.dto import SignUpInputDTO
from users.exceptions import DuplicateUser, PasswordValidationError
from users.validations import validate_password
from .service import UserService


class SignUpView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = UserService()

    def post(self, request):
        data = json.loads(request.body)

        sign_up_info = SignUpInputDTO(**data)
        try:
            validate_email(sign_up_info.email)
            validate_password(sign_up_info.password)
            self.service.add_user(sign_up_info)

        except DuplicateUser:
            return JsonResponse({"message": "USER_ALREADY_EXIST"}, status=409)

        except ValidationError:
            return JsonResponse({"message": "INVALID_EMAIL"}, status=400)

        except PasswordValidationError:
            return JsonResponse({"message": "INVALID_PASSWORD"}, status=400)
        
        else:
            return JsonResponse({"message": "CREATED"}, status=201)
