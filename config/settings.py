import os
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Settings

# ========
# SECRET_KEY and DEBUG are provided by Render as DJANGO_* env vars,
# but fall back to generic names for local development.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret-key"))
DEBUG = os.getenv("DJANGO_DEBUG", os.getenv("DEBUG", "1")) == "1"

# Hosts

# -----
# Render sets RENDER_EXTERNAL_URL like "https://your-service.onrender.com"
render_url = os.getenv("RENDER_EXTERNAL_URL")
default_hosts = ["localhost", "127.0.0.1", "testserver"]
if render_url:
    default_hosts.append(urlparse(render_url).hostname)

# Allow hosts from the environment or fall back to the defaults above.
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ",".join(default_hosts)).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ninja",
    "users",
    "tasks",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "config.multitenancy.OrganizationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}
}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DB_FILE = os.getenv("SQLITE_PATH", str(BASE_DIR / "db.sqlite3"))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DB_FILE,
    }
}
    

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

