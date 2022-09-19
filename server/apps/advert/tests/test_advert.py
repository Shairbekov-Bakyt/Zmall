from django.test import TestCase, Client
from rest_framework import status

from config.settings.local import BASE_API
from advert.api.advert_serializers import (
    AdvertListSerializer,
    AdvertCreateSerializer,
    CitySerializer
)
from user.models import CustomUser
from advert.models import Advert, Category, SubCategory, City, Promote

client = Client()


class AdvertTest(TestCase):
    ADVERT_API = BASE_API + "advert/"


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
            id =1,
            title="test",
            description="test",
            price=200,
            types="vip",
        )

        self.data_for_post = {
            "id": 1,
            "owner": self.owner.id,
            "name": "Test ad",
            "category": self.category.id,
            "sub_category": self.sub_category.id,
            "start_price": 20,
            "end_price": 200,
            "description": "Test description",
            "city": self.city.id,
            "email": "test@gmail.com",
            "wa_number": "+996500123456",
            "promote": self.promote,
        }
        self.advert = Advert.objects.create(
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

    def test_advert_post(self):

        client.login(email='test@gmail.com', password='test')
        self.data_for_post['advert_contact'] = [
                "+996500123456",
                "+996500123456",
                "+996500123456",
            ]
        self.data_for_post['promote'] = ''
        response = client.post(self.ADVERT_API, self.data_for_post)
        data_from_url = response.data
        advert = Advert.objects.get(pk=1)
        data_from_db = AdvertCreateSerializer(advert).data
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(data_from_db, data_from_url)

    def test_advert_get(self):
        response = client.get(self.ADVERT_API)
        data_from_url = response.data['results']
        advert = Advert.objects.all()
        data_from_db = AdvertListSerializer(advert, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(data_from_db, data_from_url)

    def test_advert_patch(self):
        self.data_for_post['advert_contact'] = [
            "+996500123456",
            "+996500123456",
            "+996500123456",
        ]
        self.data_for_post['promote'] = ''
        response = client.post(self.ADVERT_API, self.data_for_post)
        ADVERT_API = self.ADVERT_API + '1/'
        self.data_for_post['promote'] = {
            "promote": self.promote.id,
        }
        response = client.put(ADVERT_API, self.data_for_post)
        data_from_url = response.data
        data_from_db = CitySerializer(self.advert).data
        self.assertEqual(data_from_db, data_from_url)
        # advert = Advert.objects.get(pk=1)
        # data_from_db = AdvertCreateSerializer(advert).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual(data_from_db, data_from_url)
