import json

from advert.utils import connect_to_redis


def set_advert_views(id: int):
    view = connect_to_redis()

    if not view.exists(id):
        return 0

    advert_info = json.loads(view.get(id).decode("utf-8"))
    views_count = advert_info['views_counter']

    return views_count
