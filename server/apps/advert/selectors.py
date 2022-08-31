from django.db.models import QuerySet

from advert.models import Advert, AdvertImage


def get_advert_by_id(pk: int) -> QuerySet:
    return Advert.objects.get(id=pk)
