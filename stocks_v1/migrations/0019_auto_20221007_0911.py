# Generated by Django 3.2 on 2022-10-07 06:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stocks_v1', '0018_auto_20221007_0844'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StockNotification',
            new_name='PriceNotification',
        ),
        migrations.RenameModel(
            old_name='Tracker',
            new_name='StockTracker',
        ),
    ]