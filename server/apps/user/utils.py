from django.core.mail import EmailMessage, send_mail
from rest_framework_simplejwt.tokens import RefreshToken

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


def get_token_by_user(user):
    token = RefreshToken.for_user(user).access_token
    return str(token)
