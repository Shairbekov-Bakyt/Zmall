import json
from celery import shared_task

from advert.models import Advert, AdvertStatistics
from advert.utils import connect_to_redis
from advert.web_scraping.salexy import salexy
from advert.web_scraping.doska import doska


@shared_task
def task_salexy():
    salexy()


@shared_task
def task_doska():
    doska()


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
