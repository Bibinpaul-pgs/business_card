from rest_framework.viewsets import ViewSet
from cards.models import Card
from rest_framework.exceptions import ValidationError

from users.serializers import UserProfileSerializer, VerifyOtpSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import AllowAny

class UserViewSet(ViewSet):
    def list(self, request):
        user = request.user
        card = Card.objects.filter(created_by=user).order_by('created_by').first()
        if not card:
            raise ValidationError("Please add a card first")
        serializer = UserProfileSerializer(card, context={'request': request})

        return Response({"data": serializer.data})

class VerifyOtpViewSet(ViewSet):
    permission_classes = [AllowAny]
    def create(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        otp = serializer.validated_data.get('otp')

        user = User.objects.filter(email=email, otp=otp).first()
        if not user:
            raise ValidationError("Invalid Otp")
        user.is_verified = True
        user.otp = None
        user.save()
        return Response({"data":"Otp verified successfully"})