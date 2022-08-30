from config.celery import app as celery_app

from advert.services import send_advert_to_email


@celery_app.task
def task_send_advert_to_email(email, advert_id, advert_name):
    send_advert_to_email(email, advert_id, advert_name)
    return 1
