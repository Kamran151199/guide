
"""
    Celery configuration for the Yoona.ai project.
"""

import os
from pathlib import Path

from helpers.environ.environ import Env  # noqa # pylint: disable=import-error

BASE_DIR = Path(__file__).resolve().parent.parent.parent
env = Env(os.path.join(BASE_DIR, ".env"))

include = ["services.mailer.tasks.security"]
imports = ["services.mailer.tasks.security"]

enable_utc = os.environ.get("CELERY_ENABLE_UTC", True)
timezone = os.environ.get("CELERY_TIMEZONE", "Europe/Berlin")

CELERY_BROKER_URL = (
    f"redis://:{env.str_env('REDIS_PASSWORD')}@"
    f"{env.str_env('REDIS_HOST')}:"
    f"{env.str_env('REDIS_PORT')}/"
    f"{env.int_env('REDIS_DB')}"
)
broker_write_url = CELERY_BROKER_URL
broker_read_url = CELERY_BROKER_URL
result_backend = CELERY_BROKER_URL
broker_connection_max_retries = env.int_env("CELERY_BROKER_CONNECTION_MAX_RETRIES", 100)
