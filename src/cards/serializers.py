from rest_framework import serializers
from .models import Card, CardRequest


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            "id",
            "file",
            "profile_image",
            "full_name",
            "designation",
            "company_name",
            "phone_number",
            "email",
            "location_details",
            "card_type",
            "social_media_links",
            "created_by",
        ]


class CardRequestSerializer(serializers.ModelSerializer):
    card = CardSerializer()
    class Meta:
        model = CardRequest
        fields = ['id', 'requested_by', 'card', 'is_accepted']