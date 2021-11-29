import jwt

from django.http import JsonResponse

from .exceptions import UserNotFound
from users.models import User
from my_settings import SECRET_KEY, ALGORITHM


def authorize(func):
    def wrapper(self, request, *arg, **kwargs):
        bearer_token = request.headers.get("Authorization", None)

        if not bearer_token:
            return JsonResponse({"message": "TOKEN_DOES_NOT_EXIST"}, status=401)

        if not bearer_token.startswith("Bearer "):
            return JsonResponse({"message": "AUTHENTICATION_ERROR"}, status=401)

        try:
            access_token = bearer_token.split()[1]
            payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user = User.get_by_id(payload["id"])

        except jwt.DecodeError:
            return JsonResponse({"message": "INVALID_TOKEN"}, status=401)

        except UserNotFound:
            return JsonResponse({"message": "INVALID_USER"}, status=404)

        request.user = user
        return func(self, request, *arg, **kwargs)

    return wrapper
