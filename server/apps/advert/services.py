from user.utils import Util
from datetime import datetime

from config.settings.base import REDIS_HOST, REDIS_PORT
from apps.advert.utils import redis_connect


def send_advert_to_email(emails, advert_id, advert_name):
    absurl = "http://" + "127.0.0.1:800/api/v1/advert/" + advert_id
    email_body = f"Hi username in Zeon Mall new advert link below\n{absurl}"
    data = {
        "email_body": email_body,
        "email_subject": f"New Advert {advert_name}",
        "to_whom": emails,
    }
    Util.send_email(data)


def set_advert_count(id: int, user, ip):
    view = redis_connect(REDIS_HOST, REDIS_PORT)
    format = "%Y-%m-%d, %H:%M"
    date = str(datetime.now().strftime(format))

    if not view.exists(f'{id}_{user}_last_view'):
        d = {
            f'{id}_ip': ip,
            f'{id}_user': user,
            f'{id}_view': 0,
            f'{id}_{user}_last_view': date,
        }
        view.mset(d)

    if user == 'AnonymousUser':
        if bytes(ip, 'utf-8') not in view.get(f'{id}_ip'):
            view.incr(f'{id}_view')
            view.append(f'{id}_ip', ip)

    if bytes(user, 'utf-8') not in view.get(f'{id}_user'):
        view.incr(f'{id}_view')
        view.append(f'{id}_user', user)

    elif dates_difference(view.get(f'{id}_datetime'), format) >= 1:
        view.incr(f'{id}_view')
        view.set(f'{id}_{user}_last_view', date)


def dates_difference(date, format):
    now = datetime.now()
    dt_object = datetime.strptime(str(date).replace('b', '').replace("'", ''), format)
    diff = now - dt_object

    return diff.days
