from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OnlineShop.settings')
app = Celery('OnlineShop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
# app.autodiscover_tasks(["orders", "products"])
app.autodiscover_tasks()

# CELERY BEAT SETTINGS
app.conf.beat_schedule = {
    'send-ad-mail-every-week': {
        'task': 'products.tasks.send_ad_mails',
        'schedule': crontab(hour=15, minute=56),
        'args' : ("I am a Nigerian Prince.",)
    }
}

# celery -A OnlineShop worker -l info -P solo
