from django.test import TestCase, Client
from rest_framework.reverse import reverse

from config.settings.local import BASE_API
from advert.api.advert_serializers import (
    AdvertCreateSerializer,
    CitySerializer,
)
from advert.models import Advert, Category, SubCategory, City, Promote
from user.models import CustomUser


client = Client()


class AdvertTest(TestCase):
    ADVERT_API = BASE_API + "advert/"
    CITY_API = BASE_API + "city/"

    def setUp(self):
        CustomUser.objects.create_user(
            first_name="test owner",
            last_name="test",
            phone_number="996500123456",
            email="test@gmail.com",
            is_active=True,
            password="test",
        )
        self.owner = CustomUser.objects.get(email="test@gmail.com")
        Category.objects.create(
            id=1,
            icon="test.png",
            name="test_category",
        )
        self.category = Category.objects.get(name="test_category")
        SubCategory.objects.create(
            id=1,
            category=self.category,
            name="test_subcategory",
        )
        self.sub_category = SubCategory.objects.get(name="test_subcategory")
        self.city = City.objects.create(
            id=1,
            name="Bishkek",
        )
        self.promote = Promote.objects.create(
            title="test", description="test", price=200, types="vip"
        )

    def test_advert_post(self):
        print(self.category)
        data_for_post = {
            "owner": self.owner,
            "name": "Test ad",
            "category": self.category,
            "sub_category": self.sub_category,
            "start_price": 20,
            "end_price": 200,
            "description": "Test description",
            "city": self.city,
            "email": "test@gmail.com",
            "wa_number": "+996500123456",
            "promote": self.promote,
        }
        advert = Advert.objects.create(
            owner=self.owner,
            name="Test ad",
            category=self.category,
            sub_category=self.sub_category,
            start_price=20,
            end_price=200,
            description="Test description",
            city=self.city,
            email="test@gmail.com",
            wa_number="+996500123456",
            promote=self.promote,
        )
        client.login(email="test@gmail.com", password="test")

        response = client.post(self.ADVERT_API, data_for_post)
        data_from_url = response.data
        data_from_db = AdvertCreateSerializer(advert).data
        print(data_from_url)
        self.assertEqual(data_from_db, data_from_url)

    # def test_city(self):
    #     data_for_post = {
    #         "name": "test"
    #     }
    #     advert = City.objects.create(**data_for_post)
    #
    #     response = client.post(self.CITY_API, data_for_post)
    #     data_from_url = response.data
    #     data_from_db = CitySerializer(advert).data
    #     print(data_from_db)
    #     print(data_from_url)
    #     self.assertEqual(data_from_db, data_from_url)
