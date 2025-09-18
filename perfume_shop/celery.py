import os
from celery import Celery

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')

# Initialize Celery
app = Celery('perfume_shop')

# Configure Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery Pool Configuration
app.conf.update(
    worker_pool='solo',  # Use solo pool for low memory usage
    worker_concurrency=2,  # Limit concurrent tasks based on 1 vCPU
    task_time_limit=1800,  # 30 minute timeout per task
    task_soft_time_limit=1200,  # Soft timeout of 20 minutes
    worker_max_memory_per_child=150000,  # 150MB max memory per worker
    worker_prefetch_multiplier=1,  # Process one task at a time
)

# Auto-discover tasks
app.autodiscover_tasks()