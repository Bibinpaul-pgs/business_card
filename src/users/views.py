from rest_framework.viewsets import ViewSet
from cards.models import Card
from rest_framework.exceptions import ValidationError

from users.serializers import UserProfileSerializer
from rest_framework.response import Response

class UserViewSet(ViewSet):
    def list(self, request):
        user = request.user
        card = Card.objects.filter(created_by=user).order_by('created_by').first()
        if not card:
            raise ValidationError("Please add a card first")
        serializer = UserProfileSerializer(card, context={'request': request})

        return Response({"data": serializer.data})
