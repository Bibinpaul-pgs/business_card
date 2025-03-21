from rest_framework import serializers
from .models import Card, CardRequest, CardFile, CardKind, MyHolder
from users.serializers import UserSerializer
from django.db import transaction
from users.models import UserProfile

class CardFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardFile
        fields = ['id', 'file']


class CardSerializer(serializers.ModelSerializer):
    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        data = super().validate(data)
        if Card.objects.filter(created_by=user).count() >= 3:
            raise serializers.ValidationError("Card limit reached")
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

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        card = super().create(validated_data)
        if not UserProfile.objects.filter(user=request.user).exists():
            UserProfile.objects.create(
                user=request.user,
                profile_image=validated_data.get('profile_image'),
                full_name = validated_data.get('full_name'),
                designation = validated_data.get('designation'),
                company_name = validated_data.get('company_name'),
                phone_number = validated_data.get('phone_number'),
                email = validated_data.get('email'),
                location_details = validated_data.get('location_details')
            )
        return card

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
        data = super().validate(data)
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
    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        print("user =", user)
        data = super().validate(data)
        # Assign the requested_by field
        data["user"] = user
        print("data = ",data["card"])
        card = data["card"]
        if not card:
            raise serializers.ValidationError("Card not exist")
        
        if not card.card_type == CardKind.PUBLIC and not CardRequest.objects.filter(requested_by=request.user, card=card, is_accepted=True).exists():
            raise serializers.ValidationError("You need to request this card first")


        if MyHolder.objects.filter(**data).exists():
            raise serializers.ValidationError("This card already saved")

        return data
    class Meta:
        model = MyHolder
        fields = ['user', 'card']
        extra_kwargs = {'user': {'required': False}}
    
class MyHolderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    card = CardListSerializer()
    class Meta:
        model = MyHolder
        fields = ['user', 'card']