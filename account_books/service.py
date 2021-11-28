from .dto import CreateAccoutBookInputDTO
from .models import AccountBook
from .exceptions import AccountBookValueTypeError, InvalidTypeOfType


class CreateAccountBookService:
    def check_value_type(self, book_info: CreateAccoutBookInputDTO):
        if not (isinstance(book_info.amount, int) and\
                isinstance(book_info.category, str) and\
                isinstance(book_info.memo, str)):
            raise AccountBookValueTypeError

    def check_income_or_outlay(self, type):
        if type!=1 and type!=2:
            raise InvalidTypeOfType

    def add_account_book(self, book_info: CreateAccoutBookInputDTO, user):
        new_book = AccountBook(
            type=book_info.type,
            amount=book_info.amount,
            category=book_info.category,
            memo=book_info.memo,
            user=user
        )

        return AccountBook.add(new_book)