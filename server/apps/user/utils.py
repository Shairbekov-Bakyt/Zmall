import random
import string

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from config.settings.base import EMAIL_HOST_USER

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phonenumber_field.phonenumber import to_python


def validate_international_phonenumber(value):
    phone_number = to_python(value)
    if phone_number and not phone_number.is_valid():
        raise ValidationError(
            _("Введен неправильный формат телефона"), code="invalid_phone_number"
        )


class Util:
    @staticmethod
    def send_email(data):
        send_mail(
            subject=data["email_subject"],
            message=data["email_body"],
            from_email=EMAIL_HOST_USER,
            recipient_list=[
                data["to_whom"],
            ],
            fail_silently=False,
        )

    @staticmethod
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    @staticmethod
    def get_token_by_user(user):
        token = RefreshToken.for_user(user).access_token
        return str(token)
