from django.db import models

class UnreadMessagesQuerySet(models.QuerySet):
    def unread_for_user(self, user):
        return self.filter(read=False, receiver=user)

class UnreadMessagesManager(models.Manager):
    def get_queryset(self):
        return UnreadMessagesQuerySet(self.model, using=self._db)
    
    def unread_for_user(self, user):
        return self.get_queryset().unread_for_user(user)