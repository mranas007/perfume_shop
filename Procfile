release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: sh start.sh
worker: celery -A perfume_shop worker --loglevel=info --logfile=-