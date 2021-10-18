from pathlib import Path

LOCAL_BASE_DIR = Path(__file__).resolve().parent

LOCAL_SECRET_KEY = "your_secret_key"  # Generate with `cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1` or `base64 /dev/urandom | head -c50 -n1`
LOCAL_DEBUG = True
LOCAL_ALLOWED_HOSTS = ["127.0.0.1"]
LOCAL_DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "sample_db_name",
        "USER": "sample_user_name",
        "PASSWORD": "sample_password",
        "HOST": "localhost",
        "PORT": "",
    }
}

LOCAL_CORS_ORIGIN_WHITELIST = ("http://localhost:8080",)

LOCAL_FRONT_HOME_URL = "http://localhost:8080"

LOCAL_PUBLICATIONS_PER_PAGE = 20

LOCAL_MATOMO_DOMAIN_PATH = "matomo.example.com"
LOCAL_MATOMO_SITE_ID = "1"
