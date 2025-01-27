from rest_framework import serializers
from .models import  Message, MessageHistory, Notification
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'receiver', 'content', 'timestamp', 'edited']

    def validate_content(self, content):
        if len(content.strip()) == 0:
            raise serializers.ValidationError('Message content cannot be empty')
        return content
    
class MessageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageHistory
        fields = ['message', 'old_content', 'edited_at']
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_id', 'message', 'receiver', 'read']