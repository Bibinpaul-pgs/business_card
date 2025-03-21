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


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# local
from .models import User, UserProfile
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
    tokens = serializers.SerializerMethodField()
    # profile_id = 

    class Meta:
        model = User
        fields = ("uid", "email", "display_name", "tokens", 'user_profile')
        read_only_fields = ['uid']

    def get_tokens(self, instance):
        """ Generate JWT token for the user """
        print("instance = ", instance)
        
        refresh = RefreshToken.for_user(instance)

        if not instance.is_verified:  # Assuming `instance` has `is_verified`
            raise serializers.ValidationError("Your account is not verified. Please verify before logging in.")
        
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data


class UserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "display_name"]


class TokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        if not self.user.is_verified:
            raise serializers.ValidationError("Your account is not verified. Please verify before logging in.")

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data

class CutomObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


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
    

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'user',
            'profile_image',
            'full_name',
            'designation',
            'company_name',
            'phone_number',
            'email',
            'location_details',
        ]