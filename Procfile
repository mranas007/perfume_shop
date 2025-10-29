release: python manage.py migrate --noinput
web: sh start.sh
worker: celery -A perfume_shop worker --loglevel=info --logfile=-