from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from user.managers import UserManager


class CustomUser(AbstractUser):
    """Base user model add phone, auth_provider"""
    AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'email': 'email'}

    auth_provider = models.CharField(max_length=255, default=AUTH_PROVIDERS.get('email'))
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    phone_number = PhoneNumberField(blank=True)
    username = None

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
    ]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
