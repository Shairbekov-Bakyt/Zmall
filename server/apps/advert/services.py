from django.urls import reverse

from user.utils import Util


def send_advert_to_email(email, advert_id, advert_name):
    absurl = "http://" + "127.0.0.1:800/api/v1/advert/1"
    email_body = f"Hi username in Zeon Mall new advert link below\n{absurl}"
    data = {
        "email_body": email_body,
        "email_subject": f"New Advert {advert_name}",
        "to_whom": email,
    }
    Util.send_email(data)
