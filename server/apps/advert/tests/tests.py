from django.test import TestCase, Client

from config.settings.local import BASE_API
from advert.api.serializers import AdvertListSerializer, AdvertCreateSerializer
from advert.models import Advert, Promote, Category, SubCategory
from user.models import CustomUser
# from advert.utils import get_token_by_user

client = Client()


class AdvertTest(TestCase):
    USER_API = BASE_API + "advert/"

    def create_staff(self):
        CustomUser.objects.create_user(
            first_name="test owner",
            last_name="test",
            phone_number="996500123456",
            email="test@gmail.com",

        )
        Category.objects.create(

        )

    def test_advert_post(self):
        Advert.objects.create(
            owner="test owner",
            name="Test ad",
            category="Test category",
            sub_category="Test sub_category",
            from_price="20",
            to_price="200",
            description="Test description",
            city="Test city",
            email="test@gmail.com",
            phone_number="996500123123",
            wa_number="996500123456",
            promote="Test promote"

        )

        response = client.post(self.USER_API, self.data_for_post)
        data_from_url = response.data
        data_from_db = RegisterSerializer(data_for_check).data

        self.assertEqual(data_from_db, data_from_url)


    def test_client_verification(self):
        del self.data_for_post["policy_agreement"]
        del self.data_for_post["password2"]

        before_activate = CustomUser.objects.create_user(**self.data_for_post)
        token = get_token_by_user(before_activate)
        self.assertEqual(before_activate.is_active, False)
        url = BASE_API + "activation/?token=" + token
        response = client.get(url)

        after_activate = CustomUser.objects.get(email='admin@gmail.com')
        success_data = {"email": "Successfully activated"}
        self.assertEqual(success_data, response.data)
        self.assertEqual(after_activate.is_active, True)

