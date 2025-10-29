from .base import *
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Update this with your domains
ALLOWED_HOSTS = ['adnanfragrance.com', 'www.adnanfragrance.com', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://adnanfragrance.com', 'https://www.adnanfragrance.com']
SITE_DOMAIN = "https://www.adnanfragrance.com"



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Database
DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL")),
}

# Keep database connections open for reuse
DATABASES["default"]["CONN_MAX_AGE"] = 60

# Enforce SSL for some managed Postgres providers (set via env when needed)
if os.getenv("DB_SSL_REQUIRE", "true").lower() in ["1", "true", "yes"]:
    DATABASES["default"].setdefault("OPTIONS", {})["sslmode"] = "require"


# Static files
# Use WhiteNoise manifest storage for cache-busted filenames and compression
STORAGES["staticfiles"] = {
    "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
}


# Security settings (assumes HTTPS behind a proxy/load balancer)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True