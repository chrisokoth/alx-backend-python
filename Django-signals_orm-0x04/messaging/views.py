from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from .serializers import MessageSerializer, MessageHistorySerializer, NotificationSerializer, UserSerializer
from .models import Message, MessageHistory, Notification
from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.db.models import Prefetch
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@api_view(['DELETE'])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def get_threaded_replies(message):
    """Recursively fetch replies to a message."""
    def fetch_replies(message):
        replies = message.replies.all().select_related('sender', 'receiver')
        return [
            {
                'message': reply,
                'replies': fetch_replies(reply)
            }
            for reply in replies
        ]
    return fetch_replies(message)

class MessageViewSet(viewsets.ViewSet):

    @method_decorator(cache_page(60))
    def list(self, request):
        queryset = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        unread_messages = Message.unread.unread_for_user(request.user).only('content', 'timestamp')
        serializer = MessageSerializer(queryset, many=True)
        unread_serializer = MessageSerializer(unread_messages, many=True)
        return Response({
            'messages': serializer.data,
            'unread_messages': unread_serializer.data
        })
    
    def retrieve(self, request, pk=None):
        queryset = Message.objects.all()
        messages = Message.objects.select_related('sender', 'receiver', 'parent_message').prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
        root_message = get_object_or_404(queryset, pk=pk)
        serializer = MessageSerializer(message)
    
        response_data = serializer.data
        response_data['replies'] = get_threaded_replies(root_message)
        
        if message.sender == request.user:
            history = MessageHistory.objects.filter(message=message)
            history_serializer = MessageHistorySerializer(history, many=True)
            response_data['history'] = history_serializer.data

        return Response(response_data)

class NotificationViewSet(viewsets.ViewSet):
    queryset = Notification.objects.filter(receiver_id=request.user.user_id)

    def list(self, request):
        serializer = NotificationSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        notification = get_object_or_404(self.queryset, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

class MessageHistoryViewSet(viewsets.ViewSet):
    queryset = MessageHistory.objects.all()

    def list(self, request):
        serializer = MessageHistorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        history = get_object_or_404(self.queryset, pk=pk)
        serializer = MessageHistorySerializer(history)
        return Response(serializer.data)