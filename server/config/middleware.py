import pathlib
import time

from django.core.exceptions import SuspiciousOperation
from rest_framework.response import Response
from rest_framework import status

from advert.services import set_advert_count
from advert.utils import connect_to_redis


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class XForwardedForMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redis = connect_to_redis()
        client_ip = get_client_ip(request)
        today = time.localtime(time.time()).tm_sec
        client_count = client_ip + '_count'
        client_date = client_ip + '_date'
        if not redis.exists(client_count) and not redis.exists(client_date):
            redis.set(client_count, 0)
            redis.set(client_date, today)

        redis.incr(client_count)
        client_date = str(redis.get(client_date))[2:-1]
        client_count = int(str(redis.get(client_count))[2:-1])
        
        if int(client_date) < today:
            client_date = today
            client_count = 0
        
        if int(client_count) > 10 and client_date == today:
            raise ValueError("rate limit")

        return self.get_response(request)


class AdvertCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        advert_url = '/api/v1/advert/'
        request_url = request.path
        if request_url is None:
            return self.get_response(request)

        path = pathlib.Path(request_url)
        if str(path.parent) + '/' != advert_url:
            return self.get_response(request)

        client_ip = get_client_ip(request)
        user = request.user
        set_advert_count(int(path.name), str(user), client_ip)
        return self.get_response(request)
