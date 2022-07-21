from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

# Create your models here.


# class Investor(models.Model):
# 	investor = models.OneToOneField(User, on_delete=models.CASCADE)
# 	worth = models.DecimalField(max_digits=100, default=0, decimal_places=2)
# 	joined_date = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return self.investor.username


class Stock(models.Model):
    # investor = models.ManyToManyField(Investor, related_name='assets')
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


# class Watchlist(models.Model):
# 	watcher = models.ForeignKey(
# 		Investor, related_name="wishlist", on_delete=models.CASCADE)
# 	stock = models.ForeignKey(
# 		Stock, related_name='stocks', on_delete=models.CASCADE)
# 	price = models.DecimalField(max_digits=10, decimal_places=2)
# 	# market_price = models.DecimalField(max_digits=10, decimal_places=2)
# 	email_frequency = models.PositiveSmallIntegerField(default=1)
# 	actual_email_frequency = models.PositiveSmallIntegerField(default=0)
# 	start_date = models.DateTimeField(auto_now_add=True)
# 	completed_date = models.DateTimeField(null=True, blank=True)
# 	in_queue = models.BooleanField(default=False)
# 	status = models.BooleanField(default=False)
# 	last_email_date = models.DateTimeField(null=True, blank=True)
# 	history = HistoricalRecords()

# 	def __str__(self):
# 		return self.stock.ticker
