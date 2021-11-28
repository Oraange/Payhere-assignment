import json

from django.http import JsonResponse
from django.views import View

from core.authorizations import authorize_for_user
from .dto import CreateAccoutBookInputDTO
from .service import CreateAccountBookService
from .exceptions import AccountBookValueTypeError, InvalidTypeOfType


class CreateAccountBookView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CreateAccountBookService()

    @authorize_for_user
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        try:
            account_book_info = CreateAccoutBookInputDTO(**data)
            self.service.check_income_or_outlay(account_book_info.type)
            self.service.check_value_type(account_book_info)

        except TypeError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except InvalidTypeOfType:
            return JsonResponse({"message": "TYPE_MUST_BE_1_or_2"}, status=400)

        except AccountBookValueTypeError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
        
        else: 
            self.service.add_account_book(account_book_info, user)
            return JsonResponse({"message": "CREATED"}, status=201)
