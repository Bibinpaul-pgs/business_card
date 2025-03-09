from django.shortcuts import render
from .models import Card, CardFile, CardKind, CardRequest, MyHolder
from rest_framework import viewsets
from .serializers import (
    CardFileSerializer,
    CardListSerializer,
    CardRequestListSerializer,
    CardRequestSerializer,
    CardSerializer,
    MyHolderCreateSerializer,
    MyHolderSerializer,
)
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.filter()
    serializer_class = CardListSerializer
    filterset_fields = ["created_by", "card_type"]
    search_fields = ["full_name", "company_name"]
    ordering_fields = [
        "created_at",
    ]

    def get_queryset(self):
        return Card.objects.exclude(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return CardSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False)
    def me(self, request, pk=None):
        print("request.user = ", request.user)
        queryset = Card.objects.filter(created_by=request.user)
        serializer = CardSerializer(queryset, many=True)
        return Response({"results": serializer.data})


class CardFileViewSet(viewsets.ModelViewSet):
    queryset = CardFile.objects.filter()
    serializer_class = CardFileSerializer


class CardRequestViewSet(viewsets.ModelViewSet):
    queryset = CardRequest.objects.filter()
    serializer_class = CardRequestListSerializer

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return CardRequestSerializer
        return super().get_serializer_class()

    @action(methods=["get"], detail=False, url_path="invitations")
    def invitations(self, request, pk=None):
        user = request.user
        card_requests = CardRequest.objects.filter(
            is_accepted=False, card__created_by=user
        )
        serializer = CardRequestListSerializer(card_requests, many=True)
        return Response({"data": serializer.data})



class MyHolderViewSet(viewsets.ModelViewSet):
    queryset = MyHolder.objects.filter()
    serializer_class = MyHolderSerializer

    def get_serializer_class(self):
        if self.action == 'created' or self.action == 'update':
            return MyHolderCreateSerializer
        return super().get_serializer_class()