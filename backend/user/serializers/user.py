from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import *


class PayHereUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayHereUser
        fields = ['email', 'name', 'phone']


class PayHereUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayHereUser
        fields = ['password', 'email', 'name', 'phone']

    def create(self, validated_data):
        return PayHereUser.objects.create_user(**validated_data)

    def validate_email(self, email):
        if PayHereUser.objects.filter(email=email).exists():
            raise ValidationError('중복 이메일 입니다')
        return email


class PayHereUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = PayHereUser
        fields = ['email', 'password']
