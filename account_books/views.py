import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from core.authorizations import authorize_for_user
from .dto import (
    CreateAccoutBookInputDTO,
    ParamsInputDTO, 
    UpdateAccountBookInputDTO, 
    ReadAccountBookListOutputDTO, 
    ReadAccountBookOutputDTO
)
from .service import (
    CreateAccountBookService, 
    UpdateAccountBookService, 
    AccountBookListService,
    AccountBookDetailService
)
from .exceptions import (
    AccountBookNotFound, 
    AccountBookValueTypeError, 
    Forbidden, 
    InvalidTypeOfType
)


class AccountBookView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_service = CreateAccountBookService()
        self.get_service = AccountBookListService()

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

    @authorize_for_user
    def get(self, request):
        user = request.user
        OFFSET = request.GET.get("offset", 0)
        LIMIT = request.GET.get("limit", 5)
        try:
            params = ParamsInputDTO(offset=int(OFFSET), limit=int(LIMIT))
            account_books = self.get_service.get_account_book_list(user, params)

        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"}, status=404)

        except ValueError:
            return JsonResponse({"message": "PARAMETER_ERROR"}, status=400)

        else:
            return JsonResponse(
                {
                    "total_count": account_books.total_count,
                    "total_income": account_books.total_income,
                    "total_outlay": account_books.total_outlay,
                    "results": [
                        {
                            "updated_at": book.updated_at,
                            "type": book.type,
                            "amount": book.amount,
                            "category": book.category,
                            "memo": book.memo
                        } for book in account_books.account_books
                    ]
                }, status=200)

class AccountBookDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_service = UpdateAccountBookService()
        self.get_service = AccountBookDetailService()

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

        else:
            self.update_service.update_account_book(account_book, account_book_info)
            return HttpResponse(status=204)

    @authorize_for_user
    def get(self, request, book_id):
        user = request.user
        try:
            account_book = self.get_service.get_account_book(book_id, user)
        
        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)

        else:
            return JsonResponse(
                {
                    "updated_at": account_book.updated_at,
                    "type": account_book.type,
                    "amount": account_book.amount,
                    "category": account_book.category,
                    "memo": account_book.memo
                }, status=200)
