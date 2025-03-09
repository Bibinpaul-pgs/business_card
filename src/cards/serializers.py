from rest_framework import serializers
from .models import Card, CardRequest, CardFile, CardKind, MyHolder
from users.serializers import UserSerializer

class CardFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardFile
        fields = ['id', 'file']


class CardSerializer(serializers.ModelSerializer):
    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        print("user = ",user)
        data["created_by"] = user
        return data
    
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

class CardListSerializer(serializers.ModelSerializer):
    card_type = serializers.CharField(source='get_card_type_display')
    can_access = serializers.SerializerMethodField()
    created_by = UserSerializer()
    
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
            "can_access",
        ]

    def get_can_access(self, instance):
        if instance.card_type == CardKind.PUBLIC:
            return True
        request = self.context['request']
        if CardRequest.objects.filter(requested_by=request.user, card=instance, is_accepted=True).exists():
            return True
        return False


class CardRequestSerializer(serializers.ModelSerializer):

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        print("user =", user)

        # Assign the requested_by field
        data["requested_by"] = user

        if CardRequest.objects.filter(**data).exists():
            raise serializers.ValidationError("This request already exists")

        return data

    class Meta:
        model = CardRequest
        fields = ['id', 'requested_by', 'card', 'is_accepted']
        read_only_fields = ['requested_by'] 
    

class CardRequestListSerializer(serializers.ModelSerializer):
    card = CardSerializer()
    requested_by = UserSerializer()

    class Meta:
        model = CardRequest
        fields = ['id', 'requested_by', 'card', 'is_accepted']
        read_only_fields = ['requested_by'] 
    


class MyHolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyHolder
        fields = ['user', 'card']
    
class MyHolderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    card = CardListSerializer()
    class Meta:
        model = MyHolder
        fields = ['user', 'card']