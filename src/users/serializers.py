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


class UserProfileSerializer(serializers.Serializer):
    profile_image = serializers.ImageField()
    full_name = serializers.CharField()
    designation = serializers.CharField()
    company_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.CharField()
    location_details = serializers.CharField()
    social_media_links = serializers.JSONField()

    def to_representation(self, instance):
        request = self.context.get('request')
        data = super().to_representation(instance)

        if instance.profile_image and request is not None:
            data['profile_image'] = request.build_absolute_uri(instance.profile_image.url)

        return data