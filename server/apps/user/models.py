from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken

from user.managers import UserManager
from user.utils import validate_international_phonenumber


class CustomUser(AbstractUser):
    """Base user model add phone, auth_provider"""

    AUTH_PROVIDERS = {"facebook": "facebook", "google": "google", "email": "email"}

    auth_provider = models.CharField(
        max_length=255, default=AUTH_PROVIDERS.get("email")
    )
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    phone_number = PhoneNumberField(blank=True, validators=[validate_international_phonenumber])
    # phone_number.error_messages['invalid'] = 'Incorrect International Calling Code or Mobile Number!'
    activation_code = models.CharField(max_length=13, blank=True)
    username = None

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
    ]
    USERNAME_FIELD = "email"

    objects = UserManager()

    # def save(self):
    #     self.activation_code = Util.get_random_string(12)
    #     super().save()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
