from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from asgiref.sync import async_to_sync

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from stocks_v1.models import Stock


User = get_user_model()


class Tracker(models.Model):
    investors = models.ManyToManyField(User, related_name="subscribers")
    stock = models.ForeignKey(Stock, related_name='asset',
                              on_delete=models.CASCADE)
    quote_price = models.DecimalField(max_digits=10, decimal_places=2)
    at_tracking = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    matched = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    matched_date = models.DateTimeField(null=True, blank=True)

    def save_tracker(self):
        self.save()
        return self

    def delete_tracker(self):
        self.delete()

    @classmethod
    def get_stock(cls, id):
        stock = cls.objects.get(id=id)
        return stock

    def update_matched(self):
        self.matched_date = timezone.now()
        self.matched = True
        self.save()
        return self

    @classmethod
    def check_match(cls, id, quote_price):
        stock = cls.objects.filter(
            stock__id=id, quote_price=quote_price).first()
        return stock

    @classmethod
    def track_price(cls, stock):
        ticker = stock['ticker']
        price = float(stock['price'])
        tracker = cls.check_match(ticker, price)

        if tracker:
            tracker = tracker.update_matched()
            content = f"{ticker}'s price matches your quote of {tracker.quote_price}. Price matched at {tracker.matched_date}"
            subscribers = f"{ticker}{tracker.quote_price}"
            cls.update_clients(subscribers, content)
        return tracker

    def update_clients(subscribers, content):
        connected = get_channel_layer()
        async_to_sync(connected.group_send)(subscribers, {
            "type": "client_message", "data": content})

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.stock.ticker}: {self.quote_price}"


@receiver(pre_save, sender=Tracker)
def set_at_tracking(sender, instance, **kwargs):
    instance.at_tracking = instance.stock.price
