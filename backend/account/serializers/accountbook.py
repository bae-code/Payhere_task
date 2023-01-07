from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *


class AccountBookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBookType
        fields = '__all__'


class AccountBookSerializer(serializers.ModelSerializer):
    type = AccountBookTypeSerializer()

    class Meta:
        model = AccountBook
        fields = '__all__'


class AccountBookDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountBook
        fields = '__all__'