from config.celery import app as celery_app

from advert.services import send_advert_to_email
from user.models import CustomUser as User

@celery_app.task
def task_send_advert_to_email():
    emails = User.objects.filter(is_active=True).values_list('email', flat=True)
    send_advert_to_email(emails)
    return 1
