from multiprocessing.managers import BaseManager
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        DEVELOPER = "DEVELOPER", 'Developer'
        TRADER = "TRADER", 'Trader'
        INVESTOR = "INVESTOR", 'Investor'

    base_role = Role.INVESTOR
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class DeveloperManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=User.Role.DEVELOPER)


class Developer(User):
    base_role = User.Role.DEVELOPER
    developer = DeveloperManager()

    class Meta:
        proxy = True


class TraderManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=User.Role.TRADER)


class Trader(User):
    base_role = User.Role.TRADER
    trader = TraderManager()

    class Meta:
        proxy = True


class InvestorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=User.Role.INVESTOR)


class Investor(User):
    base_role = User.Role.INVESTOR
    investor = InvestorManager()

    class Meta:
        proxy = True


class AdminManager(BaseManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=User.Role.ADMIN)


class Admin(User):
    base_role = User.Role.ADMIN
    admin = AdminManager()

    class Meta:
        proxy = True
