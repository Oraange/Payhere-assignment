import json

from django.views import View

class SignUpInputDTO:
    name: str
    email: str
    password: str


class SignUpHandler(View):
    def __init__(self, request):
        self.data = json.loads(request.body)

    def sign_up_request(self):
        SignUpInputDTO.name = self.data["name"]
        SignUpInputDTO.email = self.data["email"]
        SignUpInputDTO.password = self.data["password"]

        return SignUpInputDTO()
