import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── 环境检测 & 安全密钥 ──────────────────────────────
IS_RAILWAY = os.environ.get("RAILWAY_ENVIRONMENT", "") != ""
SECRET_KEY = os.environ.get("SECRET_KEY", "hotel-management-secret-key-change-in-production-2026")
DEBUG = os.environ.get("DEBUG", "False" if IS_RAILWAY else "True").lower() in ("true", "1", "yes")

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = []
if IS_RAILWAY:
    public_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
    if public_domain:
        ALLOWED_HOSTS.append(public_domain)
        CSRF_TRUSTED_ORIGINS = [f"https://{public_domain}"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "accounts",
    "rooms",
    "bookings",
    "customers",
    "reports",
    "system_config",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hotel_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "hotel_management.wsgi.application"

# ── 数据库：DATABASE_URL → PostgreSQL  else → SQLite ─
DATABASE_URL = os.environ.get("DATABASE_URL", "")
if DATABASE_URL:
    import dj_database_url
    DATABASES = {"default": dj_database_url.config(default=DATABASE_URL, conn_max_age=600, conn_health_checks=True)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 6}},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = False

# ── 静态文件 (Whitenoise) ────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# ── 生产安全 ─────────────────────────────────────────
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
