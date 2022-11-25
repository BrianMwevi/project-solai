from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

from asgiref.sync import async_to_sync
from tracker.models import Tracker

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

User = get_user_model()


class PriceNotification(models.Model):
    subscriber = models.ForeignKey(
        Tracker, related_name="subscribers", on_delete=models.SET_NULL, null=True)
    viewers = models.ManyToManyField(
        User, related_name="viewed")
    content = models.CharField(max_length=255)
    viewed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    viewed_date = models.DateTimeField(blank=True, null=True)

    @classmethod
    def new_notification(cls, subscriber, content):
        instance = cls(subscriber=subscriber, content=content)
        instance.save_notification()
        return instance

    def save_notification(self):
        self.save()
        return self

    def delete_notification(self):
        self.delete()

    @classmethod
    def get_viewed(cls):
        viewed = cls.objects.filter(viewed=True)
        return viewed

    @classmethod
    def get_unviewed(cls):
        unviewed = cls.objects.filter(viewed=False)
        return unviewed

    def __str__(self):
        return self.content
