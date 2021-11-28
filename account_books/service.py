from django.db.models.query import QuerySet

from .models import AccountBook
from .dto import (
    CreateAccoutBookInputDTO,
    ReadAccountBookListOutputDTO, 
    ParamsInputDTO,
    UpdateAccountBookInputDTO
)
from .exceptions import (
    AccountBookNotFound, 
    AccountBookValueTypeError,
    Forbidden,
    InvalidTypeOfType
)


class CheckTypeValidation:
    def check_value_type(self, book_info: CreateAccoutBookInputDTO):
        if not (isinstance(book_info.amount, int) and\
                isinstance(book_info.category, str) and\
                isinstance(book_info.memo, str)):
            raise AccountBookValueTypeError

    def check_income_or_outlay(self, type):
        if type!=AccountBook.Type.INCOME.value and\
            type!=AccountBook.Type.OUTLAY.value:
            raise InvalidTypeOfType


class CheckAuthorizedUser:
    def is_authorized(self, account_book, user):
        if str(account_book.user_id)!=str(user.id):
            raise Forbidden


class CreateAccountBookService(CheckTypeValidation):
    def add_account_book(self, book_info: CreateAccoutBookInputDTO, user):
        new_book = AccountBook(
            type=book_info.type,
            amount=book_info.amount,
            category=book_info.category,
            memo=book_info.memo,
            user=user
        )

        return AccountBook.add(new_book)


class UpdateAccountBookService(CheckTypeValidation, CheckAuthorizedUser):
    def get_account_book(self, book_id):
        if not isinstance(book_id, int):
            raise AccountBookValueTypeError
        
        account_book = AccountBook.get_active_by_id(book_id)
        if not account_book:
            raise AccountBookNotFound

        return account_book

    def update_account_book(self, account_book, book_info: UpdateAccountBookInputDTO):
        account_book.type = book_info.type
        account_book.amount = book_info.amount
        account_book.category = book_info.category
        account_book.memo = book_info.memo

        account_book.save()


class AccountBookDetailService:
    def get_account_book(self, book_id):
        if not isinstance(book_id, int):
            raise AccountBookValueTypeError

        account_book = AccountBook.get_active_by_id(book_id)
        if not account_book:
            raise AccountBookNotFound

        return account_book


class AccountBookListService:
    def get_account_book_list(self, user, params: ParamsInputDTO):
        book_queryset = AccountBook.get_queryset_by_user(user)
        if not book_queryset.exists():
            raise AccountBookNotFound

        total_income = AccountBook.get_total_amount(book_queryset, AccountBook.Type.INCOME.value)
        total_outlay = AccountBook.get_total_amount(book_queryset, AccountBook.Type.OUTLAY.value)
        book_list = [*book_queryset][params.offset:params.offset+params.limit]

        return ReadAccountBookListOutputDTO(
            account_books=[book.get_details() for book in book_list],
            total_income=total_income,
            total_outlay=total_outlay,
            total_count=book_queryset.count()
        )