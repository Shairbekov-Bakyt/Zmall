import redis


def connect(host: str, port: int) -> redis.Redis:
    client = redis.Redis(host=host, port=port)
    return client


def modify_input_for_multiple_files(property_id, image):
    data = {}
    data['advert_id'] = property_id
    data['image'] = image
    return data
