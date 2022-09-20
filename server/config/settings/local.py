from .base import *
from decouple import config
import datetime


DEBUG = True
BASE_API = "http://127.0.0.1:8000/api/v1/"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": "localhost",
        "PORT": 5432,
        "TEST": {
            "NAME": "test",
        },
    }
}

REDIS_HOST = "localhost"
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