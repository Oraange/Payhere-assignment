from typing import List

from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Sum

from core.models import TimeStamp
from users.models import User
from .dto import ReadAccountBookOutputDTO

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

    def exists(self, *args, **kwargs):
        super().exists(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_details(self):
        INCOME = "income"
        OUTLAY = "outlay"
        return ReadAccountBookOutputDTO(
            updated_at=self.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            type=INCOME if self.type==AccountBook.Type.INCOME.value else OUTLAY,
            amount=self.amount,
            category=self.category,
            memo=self.memo
        )

    @classmethod
    def get_queryset_by_user(cls, user: User):
        return cls.objects.filter(user=user, is_deleted=False).order_by('-updated_at')

    @classmethod
    def get_active_by_id(cls, book_id: int):
        try:
            return cls.objects.get(id=book_id, is_deleted=False)
        
        except cls.DoesNotExist:
            None
        
    @classmethod
    def get_deactive_by_id(cls, book_id: int):
        try:
            return cls.objects.get(id=book_id, is_deleted=True)
        
        except cls.DoesNotExist:
            None

    @classmethod
    def get_total_amount(cls, books: QuerySet, type: int):
        return books.filter(type=type).aggregate(Sum('amount'))

    @classmethod
    def add(cls, account_book):
        account_book.save()
