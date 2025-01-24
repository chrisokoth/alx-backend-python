from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer


class ConversationViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and creating conversations.
    """

    @swagger_auto_schema(
        operation_description="List all conversations",
        responses={200: ConversationSerializer(many=True)},
    )
    def list(self, request):
        queryset = Conversation.objects.all()
        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new conversation",
        request_body=ConversationSerializer,
        responses={201: ConversationSerializer, 400: "Invalid data"},
    )
    def create(self, request):
        serializer = ConversationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing and sending messages.
    """

    @swagger_auto_schema(
        operation_description="List messages for a specific conversation",
        responses={200: MessageSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('conversation_id', openapi.IN_PATH, description="ID of the conversation", type=openapi.TYPE_STRING)
        ]
    )
    def list(self, request, conversation_id=None):
        queryset = Message.objects.filter(conversation_id=conversation_id)
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Send a message to a specific conversation",
        request_body=MessageSerializer,
        responses={201: MessageSerializer, 400: "Invalid data"},
        manual_parameters=[
            openapi.Parameter('conversation_id', openapi.IN_PATH, description="ID of the conversation", type=openapi.TYPE_STRING)
        ]
    )
    def create(self, request, conversation_id=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(conversation_id=conversation_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)