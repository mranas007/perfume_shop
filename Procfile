release: python manage.py shell < manage_superuser.py
web: gunicorn perfume_shop.wsgi:application --bind 0.0.0.0:8000 --workers 3 --threads 2 --worker-class=gthread --timeout 60 --preload --access-logfile - --error-logfile -
worker: celery -A perfume_shop worker --loglevel=info --logfile=-