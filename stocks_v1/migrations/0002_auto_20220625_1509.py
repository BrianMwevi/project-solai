# Generated by Django 3.2 on 2022-06-25 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_v1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalstock',
            old_name='last_update_date',
            new_name='updated_at',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='last_update_date',
            new_name='updated_at',
        ),
    ]
