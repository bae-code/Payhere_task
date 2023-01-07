from rest_framework import serializers
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
