web: gunicorn perfume_shop.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2 --worker-class gthread
worker: celery -A perfume_shop worker --loglevel=info
