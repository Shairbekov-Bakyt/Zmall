from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from .utils import Util

def send_password_with_email(user):
    password = Util.get_random_string(12)
    email_body = (
        "Hi "
        + user.first_name
        + " use password below to change your password \n"
        + password
    )

    user.set_password(password)
    user.save()

    data = {
        "email_body": email_body,
        "email_subject": "Forgot password",
        "to_whom": user.email,
    }
    Util.send_email(data)


def send_url_with_mail(user, request):
    current_site = get_current_site(request).domain
    relativeLink = reverse("email-verify")

    token = Util.get_token_by_user(user)

    absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

    email_body = "Hi " + user.first_name + " use link below to verify email \n" + absurl

    data = {
        "email_body": email_body,
        "email_subject": "Verify your email",
        "to_whom": user.email,
    }
    Util.send_email(data)