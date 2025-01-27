from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth.models import User

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=instance, receiver=instance.receiver)

@receiver(pre_save, sender=Message)
def create_message_history(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(message=instance, old_content=old_message.content)

            old_message.edited = True
            old_message.save()

@receiver(post_delete, sender=User)
def delete_user_messages(sender, instance, **kwargs):
    Message.objects.filter(Q(sender=instance)).delete()
    Notification.objects.filter(receiver=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()