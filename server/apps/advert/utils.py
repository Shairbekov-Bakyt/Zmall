import redis
from config.settings.base import REDIS_HOST, REDIS_PORT


def connect_to_redis() -> redis.Redis:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    return client

def get_request_data_for_favorite(request):
    data = dict(request.data)
    data['user_id'] = request.user.id
    return data