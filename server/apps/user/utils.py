from django.core.mail import EmailMessage, send_mail

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
            fail_silently=True
        )
