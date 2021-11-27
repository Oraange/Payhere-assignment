from uuid import uuid4

from django.db import models

from core.models import TimeStamp


class User(TimeStamp):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nick_name = models.CharField(max_length=16)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'users'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        
        if self.email==other.email:
            return True

        return False

    @classmethod
    def get_by_user_email(cls, email):
        try:
            return cls.objects.get(email=email)
        
        except cls.DoesNotExist:
            return None

    @classmethod
    def add(cls, user):
        user.save()
