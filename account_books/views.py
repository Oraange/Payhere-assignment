import json

from django.http import JsonResponse, HttpResponse
from django.views import View

from core.authorizations import authorize
from .dto import (
    BookCreateDTO,
    BookUpdateDTO,
    BookIdDTO,
    ParamsDTO
)
from .service import (
    WriteBookService,
    ReadBookService,
    DeleteBookService,
    TrashBookService
)
from .exceptions import AccountBookNotFound, Forbidden


class AccountBookView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_service = WriteBookService()
        self.get_service = ReadBookService()

    @authorize
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        try:
            input_info = BookCreateDTO(**data)
            self.create_service.check_value(input_info)

        except TypeError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

        except ValueError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
        
        else: 
            self.create_service.add_book(input_info, user)
            return JsonResponse({"message": "CREATED"}, status=201)

    @authorize
    def get(self, request):
        user = request.user
        OFFSET = request.GET.get("offset", 0)
        LIMIT = request.GET.get("limit", 5)
        try:
            params = ParamsDTO(offset=int(OFFSET), limit=int(LIMIT))
            output_info = self.get_service.get_book_list(user, params)

        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"}, status=404)

        except ValueError:
            return JsonResponse({"message": "PARAMETER_ERROR"}, status=400)

        else:
            return JsonResponse(
                {
                    "total_count": output_info.total_count,
                    "total_income": output_info.total_income,
                    "total_outlay": output_info.total_outlay,
                    "results": [
                        {
                            "id": book.id,
                            "updated_at": book.updated_at,
                            "type": book.type,
                            "amount": book.amount,
                            "category": book.category,
                            "memo": book.memo
                        } for book in output_info.books
                    ]
                }, status=200)
    

class AccountBookDetailView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_service = WriteBookService()
        self.get_service = ReadBookService()
        self.delete_service = DeleteBookService()

    @authorize
    def put(self, request, book_id):
        data = json.loads(request.body)
        user = request.user
        try:
            book_id = BookIdDTO(id=book_id)
            input_info = BookUpdateDTO(**data)
            self.update_service.check_value(input_info)
            account_book = self.update_service.get_book(book_id)
            self.update_service.is_authorized(account_book, user)

        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOK_DOES_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)
        
        except TypeError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)

        except ValueError:
            return JsonResponse({"message": "INVALID_VALUE"}, status=400)
            
        else:
            self.update_service.update_book(account_book, input_info)
            return HttpResponse(status=204)

    @authorize
    def get(self, request, book_id):
        user = request.user
        try:
            book_id = BookIdDTO(id=book_id)
            output_info = self.get_service.get_book(book_id, user)
        
        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)

        else:
            return JsonResponse(
                {
                    "id": output_info.id,
                    "updated_at": output_info.updated_at,
                    "type": output_info.type,
                    "amount": output_info.amount,
                    "category": output_info.category,
                    "memo": output_info.memo
                }, status=200)

    @authorize
    def delete(self, reqeust, book_id):
        user = reqeust.user
        try:
            book_id = BookIdDTO(id=book_id)
            self.delete_service.remove(book_id, user)
        
        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOK_DOES_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)

        else:
            return HttpResponse(status=204)


class TrashedBookView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trash_service = TrashBookService()

    @authorize
    def get(self, request):
        user = request.user
        OFFSET = request.GET.get("offset", 0)
        LIMIT = request.GET.get("limit", 5)
        try:
            params = ParamsDTO(offset=int(OFFSET), limit=int(LIMIT))
            output_info = self.trash_service.get_trash_book_list(user, params)

        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOKS_DO_NOT_EXIST"}, status=404)

        except ValueError:
            return JsonResponse({"message": "PARAMETER_ERROR"}, status=400)

        else:
            return JsonResponse(
                {
                    "total_count": output_info.total_count,
                    "results": [
                        {
                            "id": book.id,
                            "updated_at": book.updated_at,
                            "type": book.type,
                            "amount": book.amount,
                            "category": book.category,
                            "memo": book.memo
                        } for book in output_info.books
                    ]
                }, status=200)

    @authorize
    def patch(self, request, book_id):
        user = request.user
        try:
            book_id = BookIdDTO(book_=book_id)
            self.trash_service.restore(book_id, user)
        
        except AccountBookNotFound:
            return JsonResponse({"message": "ACCOUNT_BOOK_DOES_NOT_EXIST"}, status=404)

        except Forbidden:
            return JsonResponse({"message": "FORBIDDEN"}, status=403)

        else:
            return JsonResponse({"message": "PUBLISHED"}, status=200)
