from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'qr_otp', 'phone_number', 'mail_otp', 'email', 'backup_code']