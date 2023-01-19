from django.db import models
from django.apps import apps
from django.db.models import Sum, F, Count
from ..choices import *


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
                             choices=ACCOUNT_BOOK_TYPE_CHOICES,
                             default=NON_TYPE)
    use_amount = models.IntegerField()
    memo = models.CharField(max_length=255,
                            null=True,
                            blank=True)

    is_archived = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_use_amount_stat(self):
        """
        유저 가계부 사용 통계 Queryset
        """
        type_stats = self.values('type').annotate(
            sum_value=Sum('use_amount'),
            type_qty=Count('id'),
            type_name=F('type__name')
        ).values('type_name', 'type_qty', 'sum_value')

        total_stat = type_stats.aggregate(Sum('type_qty'), Sum('sum_value'))

        stat = {
            'total_amount': total_stat['sum_value__sum'],
            'type_amount': {},
            'type_percent': {}
        }

        for type_stat in type_stats:
            percent = round(type_stat['type_qty'] / total_stat['type_qty__sum'] * 100, 2)
            stat['type_amount'][type_stat['type_name']] = type_stat['sum_value']
            stat['type_percent'][type_stat['type_name']] = percent

        return stat
