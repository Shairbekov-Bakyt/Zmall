from django.test import TestCase, Client
from rest_framework import status
from rest_framework.reverse import reverse

from config.settings.local import BASE_API
from advert.serializers.advert_serializers import (
    AdvertCreateSerializer,
    CitySerializer,
)
from advert.models import Advert, Category, SubCategory, City, Promote
from user.models import CustomUser

client = Client()


class AdvertTest(TestCase):
    CITY_API = BASE_API + "city/"

    City.objects.create(name='test')

