import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')
app = Celery('perfume_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()