from django.shortcuts import render
from .models import Card, CardKind, CardRequest
from rest_framework import viewsets
from .serializers import CardRequestSerializer, CardSerializer
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response


# Create your views here.

class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.filter()
    serializer_class = CardSerializer
    filterset_fields = ['created_by', 'card_type']
    search_fields = ['full_name', 'company_name']
    ordering_fields = ['created_at', ]

    @action(methods=['get'], detail=False)
    def me(self, request, pk=None):
        queryset = Card.objects.filter()
        serializer = CardSerializer(queryset, many=True)
        return Response({"results": serializer.data})
    

    @action(methods=['get'], detail=True, url_path='request')
    def request_card(self, request, pk=None):
        object = self.get_object()
        request, created = CardRequest.objects.get_or_create(card=object)
        if not created:
            return Response({"data": "request already created"})
        return Response({"data": "request created"})
    
    @action(methods=['get'], detail=False, url_path='invitations')
    def invitations(self, request, pk=None):
        card_requests = CardRequest.objects.filter(is_accepted=False)
        serializer = CardRequestSerializer(card_requests, many=True)
        return Response({"data": card_requests.data})





