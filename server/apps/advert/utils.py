import hashlib
import json
import requests
import redis
from decouple import config
from bs4 import BeautifulSoup
from collections import OrderedDict
from django.conf import settings

from advert.models import Transaction
from user.utils import Util


def connect_to_redis():
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

    return hashed_sig(data, method)


def generate_status_sig(order_id, method) -> dict:
    data = dict(
        pg_order_id=order_id,
        pg_merchant_id=config("PG_MERCHANT_ID"),
        pg_salt=Util.get_random_string(30),
    )

    return hashed_sig(data, method)


def hashed_sig(data, method):
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


def get_status_content(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('pg_transaction_status').text


def get_payment_details(params, method):
    response = requests.post(url=config("PAYBOX_BASE_URL")+method, params=params)

    if "status" in method:
        url = get_status_content(response.content)
    else:
        url = get_url_from_content(response.content)

    return url


def set_status(order_id: int):
    method = "get_status2.php"
    params = generate_status_sig(order_id, method)
    status = get_payment_details(params, method)
    order = Transaction.objects.get(pk=order_id)

    failed = ["failed", "refunded", "revoked", "incomplete"]

    if status == "ok":
        order.status = "success"
    elif status in failed:
        order.status = "failed"
    else:
        order.status = "pending"
    order.save()


def get_views(instance):
    view = connect_to_redis()
    redis_views = view.get(instance.id)
    ad_views = 0

    if redis_views is not None:
        redis_views = json.loads(redis_views.decode("utf-8"))
        ad_views = redis_views['views_counter']

    return ad_views
