from django.db import models
from simple_history.models import HistoricalRecords


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
