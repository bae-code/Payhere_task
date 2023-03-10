from rest_framework import serializers
from ..models import *


class AccountBookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBookType
        fields = '__all__'


class AccountBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBook
        fields = ['type', 'use_amount', 'memo']


class AccountBookDetailSerializer(serializers.ModelSerializer):
    type = AccountBookTypeSerializer()

    class Meta:
        model = AccountBook
        fields = '__all__'
