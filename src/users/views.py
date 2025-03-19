from rest_framework.viewsets import ViewSet,ModelViewSet
from cards.models import Card
from rest_framework.exceptions import ValidationError

from users.serializers import UserProfileSerializer, VerifyOtpSerializer
from rest_framework.response import Response
from .models import User, UserProfile
from rest_framework.permissions import AllowAny

class UserViewSet(ModelViewSet):
    queryset = UserProfile.objects.filter()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        queryset = UserProfile.objects.filter(user=self.request.user)
        return queryset

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