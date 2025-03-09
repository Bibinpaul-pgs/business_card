# users/serializers.py
# builtins
import re

# django rest framework
from rest_framework import serializers
from django.db import transaction

# third party
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)


# local
from .models import User
import uuid


class UserCreateSerializer(BaseUserCreateSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['uid'] = uuid.uuid4()
        return data
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ("uid", "email", "display_name", "password")
        read_only_fields = ['uid']


class UserSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ("uid", "email", "display_name")
        read_only_fields = ['uid']


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "display_name"]