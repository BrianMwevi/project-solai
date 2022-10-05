from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from simple_history.models import HistoricalRecords
from django.conf import settings
from django.shortcuts import get_object_or_404


class Stock(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=20, null=True, blank=True, unique=True)
    ticker = models.CharField(max_length=10, unique=True)
    volume = models.PositiveIntegerField(default=0.00)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    prev_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    open_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    percentage_change = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    min_price = models.DecimalField(
        max_digits=10, default=0, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(related_name='logs')

    @classmethod
    def get_stock(cls, id):
        stock = cls.objects.get(id=id)
        return stock

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.ticker


class Tracker(models.Model):
    investors = models.ManyToManyField(
        settings.AUTH_USER_MODEL)
    stock = models.ForeignKey(Stock, related_name='asset',
                              on_delete=models.CASCADE)
    quote_price = models.DecimalField(max_digits=10, decimal_places=2)
    at_tracking = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    matched = models.BooleanField(default=False)
    start_date = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now_add=True)
    matched_date = models.DateField(null=True, blank=True)

    @classmethod
    def get_stock(cls, id):
        stock = cls.objects.get(id=id)
        return stock

    @classmethod
    def check_stock(cls, ticker, quote_price):
        stock = cls.objects.filter(
            stock__ticker=ticker, quote_price=quote_price).first()
        return stock

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return f"{self.stock.ticker}: {self.quote_price}"


class Notification(models.Model):
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="subscribers")
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="viewed")
    source = models.CharField(max_length=25)
    content = models.CharField(max_length=255)
    viewed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    viewed_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.content


@receiver(pre_save, sender=Tracker)
def set_at_tracking(sender, instance, **kwargs):
    instance.at_tracking = instance.stock.price
