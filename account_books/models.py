from django.db import models

from core.models import TimeStamp


class AccountBook(TimeStamp):
    
    class Type(models.IntegerChoices):
        INCOME = 1
        OUTLAY = 2
    
    type = models.IntegerField(choices=Type.choices)
    amount = models.PositiveIntegerField(db_index=True)
    category = models.CharField(max_length=128)
    memo = models.TextField()
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'account_books'
