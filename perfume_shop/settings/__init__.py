import os


# Allow using DJANGO_SETTINGS_MODULE=perfume_shop.settings
# Select settings module based on DJANGO_ENV env var
# - DJANGO_ENV=production → use production settings
# - otherwise → use development settings
env = os.getenv("DJANGO_ENV", "development").lower()

if env == "production":
    from .production import *  # noqa: F401,F403
else:
    from .development import *  # noqa: F401,F403