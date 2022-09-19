from .base import *
from decouple import config
import datetime

DEBUG = False

ALLOWED_HOSTS = ["188.225.83.42", "0.0.0.0"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": 5432,
    }
}

REDIS_HOST = "redis"
REDIS_PORT = 6379
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_BROKER_URL = "redis://" + REDIS_HOST + ":" + str(REDIS_PORT)
CELERY_RESULT_BACKEND = "redis://" + REDIS_HOST + ":" + str(REDIS_PORT)
CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": 3600}
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

JWT_AUTH = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=2),
    'JWT_ALLOW_REFRESH': True,
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
}