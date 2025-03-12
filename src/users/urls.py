# django
from django.urls import include, path
from .serializers import CutomObtainPairView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/jwt/create/', CutomObtainPairView.as_view(), name='customtoken'),
    path('auth/', include('djoser.urls.jwt')),
]