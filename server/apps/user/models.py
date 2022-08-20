from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from user.managers import UserManager


class CustomUser(AbstractUser):
    """Base user model add phone, policy agreement"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True
        )
    username = models.CharField(max_length=25, blank=True, unique=False)
    phone_number = PhoneNumberField(blank=True)
    policy_agreement = models.BooleanField()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'policy_agreement',]
    USERNAME_FIELD = 'email'
    
    objects = UserManager()
