from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# User Model extending AbstractUser
class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)  # Ensure email is unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    # Explicitly define the password field (optional but may be needed for checks)
    password = models.CharField(max_length=128)  # Default length for hashed passwords

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Conversation Model
class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id} with {self.participants.count()} participants"
    


# Message Model
class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Add created_at field if needed

    def __str__(self):
        return f"Message from {self.sender.email} in conversation {self.conversation.conversation_id} at {self.sent_at}"