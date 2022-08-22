import redis


def connect(host: str, port: int) -> redis.Redis:
    client = redis.Redis(host=host, port=port)
    return client
