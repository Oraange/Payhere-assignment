from typing import List

from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Sum

from core.models import TimeStamp
from users.models import User
from .dto import BookOutputDTO


class AccountBook(TimeStamp):
    
    class Type(models.IntegerChoices):
        INCOME = 1
        OUTLAY = 2
    
    type = models.IntegerField(choices=Type.choices)
    amount = models.PositiveIntegerField(db_index=True)
    category = models.CharField(max_length=128)
    memo = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_books'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.id == other.id:
            return True
        
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_details(self):
        INCOME = "income"
        OUTLAY = "outlay"
        return BookOutputDTO(
            id=self.id,
            updated_at=self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            type=INCOME if self.type==AccountBook.Type.INCOME.value else OUTLAY,
            amount=self.amount,
            category=self.category,
            memo=self.memo
        )

    @classmethod
    def get_queryset_by_user(cls, user: User, **flag: bool):
        return cls.objects.filter(user=user, **flag).order_by('-updated_at')

    @classmethod
    def get_by_id(cls, book_id: int, **flag: bool):
        try:
            return cls.objects.get(id=book_id, **flag)
        
        except cls.DoesNotExist:
            None

    @classmethod
    def get_total_amount(cls, books: QuerySet):
        return books.filter(type=1).aggregate(Sum('amount'))["amount__sum"],\
            books.filter(type=2).aggregate(Sum('amount'))["amount__sum"]

    @classmethod
    def add(cls, account_book):
        account_book.save()
