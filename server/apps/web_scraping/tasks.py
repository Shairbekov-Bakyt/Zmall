from celery import shared_task

from .salexy import salexy
from .doska import doska

@shared_task
def task_salexy():
    salexy()

@shared_task
def task_doska():
    doska()

