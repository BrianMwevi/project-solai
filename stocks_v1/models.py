from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from simple_history.models import HistoricalRecords
from django.conf import settings


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

    class Meta:
        ordering = ['updated_at']

    def __str__(self):
        return self.ticker


class Tracker(models.Model):
    investor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, related_name='asset',
                              on_delete=models.CASCADE)
    quote = models.DecimalField(max_digits=10, decimal_places=2)
    at_tracking = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    in_queue = models.BooleanField(default=False)
    start_date = models.DateField(auto_now=True)
    last_updated = models.DateField(auto_now_add=True)
    completed = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.stock.ticker


@receiver(pre_save, sender=Tracker)
def set_at_tracking(sender, instance, **kwargs):
    instance.at_tracking = instance.stock.price
