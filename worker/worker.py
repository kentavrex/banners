from worker.tasks import *  # NOQA
from celery import Celery
from config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND
celery.conf.result_backend_transport_options = {
    'global_keyprefix': f"{settings.APP_REDIS_PREFIX}:"
}
celery.conf.timezone = settings.TIMEZONE
