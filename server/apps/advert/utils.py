import re

import redis
from django.conf import settings


def connect_to_redis() -> redis.Redis:
    client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    return client


def get_request_data_for_favorite(request):
    data = dict(request.data)
    data["user_id"] = request.user.id
    return data


def get_price_from_description(data: str) -> int:
    return 10
