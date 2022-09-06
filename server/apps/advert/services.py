from user.utils import Util


def send_advert_to_email(emails, advert_id, advert_name):
    absurl = "http://" + "127.0.0.1:800/api/v1/advert/" + advert_id
    email_body = f"Hi username in Zeon Mall new advert link below\n{absurl}"
    data = {
        "email_body": email_body,
        "email_subject": f"New Advert {advert_name}",
        "to_whom": emails,
    }
    Util.send_email(data)
