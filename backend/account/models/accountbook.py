from django.db import models
from django.apps import apps


class AccountBookType(models.Model):
    name = models.CharField(max_length=50)


class AccountBook(models.Model):
    user = models.ForeignKey('user.PayHereUser',
                             db_column='user_id',
                             related_name='accountbook',
                             on_delete=models.CASCADE)
    type = models.ForeignKey('AccountBookType',
                             db_column='type_id',
                             related_name='accountbook',
                             on_delete=models.SET_DEFAULT,
                             default=1)
    use_amount = models.IntegerField()
    memo = models.CharField(max_length=255,
                            null=True,
                            blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
