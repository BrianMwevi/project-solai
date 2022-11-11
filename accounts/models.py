import uuid
from multiprocessing.managers import BaseManager
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework_api_key.models import APIKey


class User(AbstractUser):
    """Defines custom user objects -- Developer, Investor and Trader. Default user role is developer"""

    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'Admin'
        DEVELOPER = "DEVELOPER", 'Developer'
        TRADER = "TRADER", 'Trader'
        INVESTOR = "INVESTOR", 'Investor'

    class Usage(models.TextChoices):
        STUDENT = "STUDENT", 'Student'
        BUSINESS = "BUSINESS", 'Business'
        PERSONAL = "PERSONAL", 'Personal'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usage = models.CharField(max_length=55, choices=Usage.choices)
    role = models.CharField(max_length=55, choices=Role.choices)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    api_key = models.ForeignKey(
        APIKey, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_apikey')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @classmethod
    def get_user_by_email(cls, email):
        return cls.objects.filter(email__iexact=email).first()

    @classmethod
    def get_user(cls, id):
        return cls.objects.get(id=id)


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
