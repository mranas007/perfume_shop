import os
from celery import Celery

# This is the crucial line for Windows users
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
app = Celery('perfume_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()