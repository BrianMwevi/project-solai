import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from rest_framework_api_key.models import APIKey


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Defines a custom user with a role and reason for app usage"""

    objects = CustomUserManager()

    class Roles(models.TextChoices):
        DEVELOPER = "DEVELOPER", 'Developer'
        TRADER = "TRADER", 'Trader'
        INVESTOR = "INVESTOR", 'Investor'

    class Usage(models.TextChoices):
        STUDENT = "STUDENT", 'Student'
        PERSONAL = "PERSONAL", 'Personal'
        BUSINESS = "BUSINESS", 'Business'

    username = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    usage = models.CharField(max_length=20, choices=Usage.choices)
    role = models.CharField(max_length=20, choices=Roles.choices)
    email = models.EmailField(_('email address'), unique=True)
    api_key = models.ForeignKey(
        APIKey,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='user_apikey')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def group(self):
        groups = self.groups.all()
        return groups[0].name if groups else None

    @classmethod
    def get_user(cls, id):
        return cls.objects.get(id=id)
    @classmethod
    def get_user_by_email(cls, email):
        return cls.objects.get(email=email)
        
    def __str__(self):
        return f"{self.email}"
