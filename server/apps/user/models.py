from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from user.managers import UserManager


class CustomUser(AbstractUser):
    """Base user model add phone, policy agreement"""

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

