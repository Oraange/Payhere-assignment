from .models import AccountBook, User
from .dto import (
    BookCreateDTO,
    BookUpdateDTO,
    BookIdDTO,
    BookListOutputDTO, 
    ParamsDTO,
    TreshListOutputDTO,
)
from .exceptions import AccountBookNotFound, Forbidden


class PermissionService:
    def is_authorized(self, book: AccountBook, user: User):
        if str(book.user_id)!=str(user.id):
            raise Forbidden


class WriteBookService(PermissionService):
    def check_value(self, input_info):
        if not (isinstance(input_info.amount, int) and\
                isinstance(input_info.category, str) and\
                isinstance(input_info.memo, str)) or\
            (input_info.type!=AccountBook.Type.INCOME.value and\
            input_info.type!=AccountBook.Type.OUTLAY.value) or\
            input_info.amount<0:
            raise ValueError

    def add_book(self, input_info: BookCreateDTO, user):
        new_book = AccountBook(
            type=input_info.type,
            amount=input_info.amount,
            category=input_info.category,
            memo=input_info.memo,
            user=user
        )
        AccountBook.add(new_book)

    def get_book(self, book: BookIdDTO):
        account_book = AccountBook.get_by_id(book.id, is_deleted=False)
        if not account_book:
            raise AccountBookNotFound

        return account_book

    def update_book(self, account_book: AccountBook, input_info: BookUpdateDTO):
        account_book.type = input_info.type
        account_book.amount = input_info.amount
        account_book.category = input_info.category
        account_book.memo = input_info.memo

        account_book.save()


class ReadBookService(PermissionService):
    def get_book(self, book: BookIdDTO, user: User):
        account_book = AccountBook.get_by_id(book.id, is_deleted=False)
        if not account_book:
            raise AccountBookNotFound
        super().is_authorized(account_book, user)

        return account_book.get_details()

    def get_book_list(self, user, params: ParamsDTO):
        books = AccountBook.get_queryset_by_user(user, is_deleted=False)
        if not books.exists():
            raise AccountBookNotFound

        total_income, total_outlay = AccountBook.get_total_amount(books)
        book_list = [*books][params.offset:params.offset+params.limit]

        return BookListOutputDTO(
            books=[book.get_details() for book in book_list],
            total_income=total_income or 0,
            total_outlay=total_outlay or 0,
            total_count=books.count()
        )


class DeleteBookService(PermissionService):
    def remove(self, book: BookIdDTO, user: User):
        account_book = AccountBook.get_by_id(book.id, is_deleted=False)
        if not account_book:
            raise AccountBookNotFound

        super().is_authorized(account_book, user)
        account_book.is_deleted = True
        account_book.save()


class TrashBookService(PermissionService):
    def restore(self, book: BookIdDTO, user: User):
        deleted_account_book = AccountBook.get_by_id(book.id, is_deleted=True)
        if not deleted_account_book:
            raise AccountBookNotFound

        super().is_authorized(deleted_account_book, user)
        deleted_account_book.is_deleted = False
        deleted_account_book.save()

    def get_trash_book_list(self, user, params: ParamsDTO):
        books = AccountBook.get_queryset_by_user(user, is_deleted=True)
        if not books.exists():
            raise AccountBookNotFound

        book_list = [*books][params.offset:params.offset+params.limit]

        return TreshListOutputDTO(
            account_books=[book.get_details() for book in book_list],
            total_count=books.count()
        )