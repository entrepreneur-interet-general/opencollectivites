from pathlib import Path

from .settings import INSTALLED_APPS

BASE_DIR = Path(__file__).resolve().parent

INSTALLED_APPS += ["django_extensions"]

SECRET_KEY = "your_secret_key"  # Generate with `cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1` or `base64 /dev/urandom | head -c50 -n1`
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "sample_db_name",
        "USER": "sample_user_name",
        "PASSWORD": "sample_password",
        "HOST": "localhost",
        "PORT": "",
    }
}

# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:8080",)

# Matomo
MATOMO_DOMAIN_PATH = "matomo.example.com"
MATOMO_SITE_ID = "1"

FRONT_HOME_URL = "http://localhost:8080"
PUBLICATIONS_PER_PAGE = 20
