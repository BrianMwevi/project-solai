from multiprocessing.managers import BaseManager
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):
    """Defines custom user objects -- Developer, Investor and Trader. Default user is developer"""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        DEVELOPER = "DEVELOPER", 'Developer'
        TRADER = "TRADER", 'Trader'
        INVESTOR = "INVESTOR", 'Investor'

    class Usage(models.TextChoices):
        STUDENT = "STUDENT", 'Student'
        BUSINESS = "BUSINESS", 'Business'
        PERSONAL = "PERSONAL", 'Personal'

    base_role = Role.DEVELOPER
    usage = models.CharField(max_length=55, choices=Usage.choices)
    role = models.CharField(max_length=55, choices=Role.choices)
    is_confirmed = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            if self.base_role == "ADMIN":
                self.is_superuser = True
                self.is_staff = True
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
