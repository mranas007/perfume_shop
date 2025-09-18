"""
WSGI config for perfume_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
print("Loading WSGI application...")

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'perfume_shop.settings')

application = get_wsgi_application()

print("WSGI application initialized!")