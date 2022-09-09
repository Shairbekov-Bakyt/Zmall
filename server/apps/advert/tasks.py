from celery import shared_task

from config.celery import app as celery_app

from advert.services import send_advert_to_email
from user.models import CustomUser as User


@shared_task
def task_send_advert_to_email():
    emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
    send_advert_to_email(emails)
    return 1
