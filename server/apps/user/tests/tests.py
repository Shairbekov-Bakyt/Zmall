from django.test import TestCase, Client

from config.settings.local import BASE_API
from user.api.serializers import RegisterSerializer
from user.models import CustomUser
from user.selectors import get_user_by_email
from user.utils import get_token_by_user

client = Client()


class UserTest(TestCase):
    USER_API = BASE_API + "user/register/"
    data_for_post = {
        "last_name": "test_last_name",
        "first_name": "test_first_name",
        "email": "admin@gmail.com",
        "phone_number": "+996999312292",
        "policy_agreement": True,
        "password": "admin12345",
        "password2": "admin12345",
    }

    def test_client_post(self):
        data_for_check = {
            "last_name": "test_last_name",
            "first_name": "test_first_name",
            "email": "admin@gmail.com",
            "phone_number": "+996999312292",
        }

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
        url = BASE_API + "user/activation/?token=" + token
        response = client.get(url)

        after_activate = get_user_by_email("admin@gmail.com")
        success_data = {"email": "Successfully activated"}
        self.assertEqual(success_data, response.data)
        self.assertEqual(after_activate.is_active, True)
