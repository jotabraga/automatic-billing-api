from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kanastra.settings")
app = Celery("kanastra")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

import django_celery_results


# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")
