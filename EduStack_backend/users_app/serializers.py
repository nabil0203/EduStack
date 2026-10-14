from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'mobile_no']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(source='mobile_no')

    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'first_name', 'last_name']
