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
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'account_books'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        if self.id == other.id:
            return True
        
        return False

    @classmethod
    def get_list_by_user_id(cls, user):
        if not cls.objects.filter(user=user).exists():
            return None

        return cls.objects.filter(user=user)

    @classmethod
    def get_active_by_id(cls, book_id):
        try:
            return cls.objects.get(id=book_id, is_deleted=False)
        
        except cls.DoesNotExist:
            None

    @classmethod
    def get_deactive_by_id(cls, book_id):
        try:
            return cls.objects.get(id=book_id, is_deleted=True)
        
        except cls.DoesNotExist:
            None

    @classmethod
    def add(cls, account_book):
        account_book.save()
