import random
import string

from django.core.mail import send_mail
from config.settings.base import EMAIL_HOST_USER


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
            fail_silently=True,
        )

    @staticmethod
    def get_random_string(length):
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str
