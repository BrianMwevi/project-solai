# Generated by Django 3.2 on 2022-06-25 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks_v1', '0004_auto_20220625_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stock',
            options={'ordering': ['updated_at']},
        ),
        migrations.RenameField(
            model_name='historicalstock',
            old_name='change',
            new_name='percentage_change',
        ),
        migrations.RenameField(
            model_name='stock',
            old_name='change',
            new_name='percentage_change',
        ),
    ]
