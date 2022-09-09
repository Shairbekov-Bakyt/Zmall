from user.utils import Util
from datetime import datetime

from advert.utils import connect_to_redis
from advert.models import Advert


def send_advert_to_email(emails):
    absurl = [f"http://" + "127.0.0.1:800/api/v1/advert/{i}" for i in Advert.objects.filter(status='act').order_by('-created_date').values_list('id', flat=True)]
    urls = '\n'.join(absurl)
    email_body = f"Hi username in Zeon Mall new advert link below\n{urls}"
    data = {
        "email_body": email_body,
        "email_subject": f"News Advert",
        "to_whom": emails,
    }
    Util.send_email(data)


def set_advert_count(id: int, user, ip):
    view = connect_to_redis()
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

    elif dates_difference(view.get(f'{id}_{user}_last_view'), format) >= 1:
        view.incr(f'{id}_view')
        view.set(f'{id}_{user}_last_view', date)


def dates_difference(date, format):
    now = datetime.now()
    dt_object = datetime.strptime(str(date).replace('b', '').replace("'", ''), format)
    diff = now - dt_object

    return diff.days
