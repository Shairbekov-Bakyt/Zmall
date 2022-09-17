import json

from celery import shared_task, Celery, schedules

from advert.services import send_advert_to_email
from advert.models import Advert, AdvertStatistics
from advert.utils import connect_to_redis
from user.models import CustomUser as User

app = Celery()


# @shared_task
# def task_send_advert_to_email():
#     emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
#     send_advert_to_email(emails)
#     return 1


app.conf.save_advert_statistics_schedule = {
    "add-every-morning": {
        "task": "tasks.add",
        "schedule": schedules.crontab(minute="*/2"),
        "args": (16, 16),
    },
}


@shared_task
def task_save_advert_statistics():
    adverts = Advert.objects.filter(status="act")

    rd = connect_to_redis()

    statistics = []
    for advert in adverts:
        id = advert.id
        if not rd.exists(id):
            continue

        contacts_views = 0
        if rd.exists(f"{id}-contacts"):
            advert_contacts_views = json.loads(rd.get(f"{id}-contacts").decode("utf-8"))
            contacts_views = advert_contacts_views["views_counter"]

        advert_views = json.loads(rd.get(id).decode("utf-8"))
        statistics.append(
            AdvertStatistics(
                advert=advert,
                advert_contacts_view=contacts_views,
                advert_views=advert_views["views_counter"],
            )
        )

    AdvertStatistics.objects.bulk_create(statistics)
