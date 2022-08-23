from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken

from .utils import Util


def send_token_with_mail(user, request):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relativeLink = reverse("email-verify")

    absurl = "http://" + current_site + relativeLink + "?token=" + str(token)

    email_body = "Hi " + user.first_name + " use link below to verify email \n" + absurl

    data = {
        "email_body": email_body,
        "email_subject": "Verify your email",
        "to_whom": user.email,
    }
    Util.send_email(data)
