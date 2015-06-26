from __future__ import absolute_import
__author__ = 'dAKE'

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTING_MODULE', 'partner_sys.settings')

from django.conf import settings

app = Celery('partner_sys', broker='amqp://guest:guest@localhost:5672/', backend='amqp://guest:guest@localhost:5672/')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))