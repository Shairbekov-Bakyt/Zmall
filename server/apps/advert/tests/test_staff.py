from django.test import TestCase, Client

from config.settings.local import BASE_API
from advert.models import City

client = Client()


class AdvertTest(TestCase):
    CITY_API = BASE_API + "city/"

    City.objects.create(name='test')

