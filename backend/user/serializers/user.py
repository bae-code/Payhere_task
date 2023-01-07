from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *


class PayHereUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField()
    password = serializers.CharField()
    phone = serializers.CharField()

    class Meta:
        model = PayHereUser
        fields = '__all__'

    def create(self, validated_data):
        return PayHereUser.objects.create_user(**validated_data)

    def validate_email(self, email):
        if PayHereUser.objects.filter(email=email).exists():
            raise ValidationError('중복 이메일 입니다')
