import hashlib
from bs4 import BeautifulSoup
from collections import OrderedDict

from django.conf import settings


import redis
from decouple import config

from user.utils import  Util

def connect_to_redis() -> redis.Redis:
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return client


def get_request_data_for_favorite(request):
    data = dict(request.data)
    data["user_id"] = request.user.id
    return data


def get_price_from_description(data: str) -> int:
    return 10


def generate_sig(data: dict, method: str) -> dict:
    data = dict(
        pg_order_id=data.id,
        pg_merchant_id=config("PG_MERCHANT_ID"),
        pg_amount=data.price,
        pg_description=data.description,
        pg_salt=Util.get_random_string(30),
        pg_success_url='https://localhost:3000/',
    )
    data = OrderedDict(sorted(data.items()))
    string = method
    for key, value in data.items():
        if value and key != 'pg_sig':
            string += ";{}".format(value)

    string += ";{}".format("LeFnP16MP6AU6YKc")
    pg_sig = hashlib.md5(string.encode()).hexdigest()
    data['pg_sig'] = pg_sig
    return data


def get_url_from_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('pg_redirect_url').text
