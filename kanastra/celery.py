from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanastra.settings")
app = Celery("kanastra")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# add logs to celery
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler("celery.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

app.log.setup(loglevel=logging.INFO, logfile="celery.log")
