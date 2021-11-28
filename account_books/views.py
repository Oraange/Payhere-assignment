import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from core.authorizations import authorize_for_user
from .dto import CreateAccoutBookInputDTO, UpdateAccountBookInputDTO
from .service import CreateAccountBookService, UpdateAccountBookService
from .exceptions import AccountBookNotFound, AccountBookValueTypeError, Forbidden, InvalidTypeOfType


class AccountBookView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_service = CreateAccountBookService()

    @authorize_for_user
    def post(self, request):
        data = json.loads(request.body)
        user = request.user

        try:
            account_book_info = CreateAccoutBookInputDTO(**data)
            self.create_service.check_income_or_outlay(account_book_info.type)
            self.create_service.check_value_type(account_book_info)

        except TypeError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except InvalidTypeOfType:
            return JsonResponse({"message": "TYPE_MUST_BE_1_or_2"}, status=400)

        except AccountBookValueTypeError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
        
        else: 
            self.create_service.add_account_book(account_book_info, user)
            return JsonResponse({"message": "CREATED"}, status=201)


class AccountBookDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_service = UpdateAccountBookService()

    @authorize_for_user
    def put(self, request, book_id):
        data = json.loads(request.body)
        user = request.user
        try:
            account_book_info = UpdateAccountBookInputDTO(**data)
            account_book = self.update_service.get_account_book(book_id)
            self.update_service.is_authorized(account_book, user)
            self.update_service.check_income_or_outlay(account_book_info.type)
            self.update_service.check_value_type(account_book_info)

        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOK_DOES_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)
        
        except TypeError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

        except InvalidTypeOfType:
            return JsonResponse({"message": "TYPE_MUST_BE_1_or_2"}, status=400)

        except AccountBookValueTypeError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)

        else:
            self.update_service.update_account_book(account_book, account_book_info)
            return HttpResponse(status=204)
