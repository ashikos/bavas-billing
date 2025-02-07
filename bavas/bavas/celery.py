from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from django.conf import settings
# settings.py
from os.path import expanduser
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bavas.settings')

app = Celery('bavas')
app.conf.update(timezone='Asia/Kolkata')

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'request: {self.request!r}')