import os
from celery import Celery

os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_config")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("Guide")
app.config_from_envvar("CELERY_CONFIG_MODULE")
