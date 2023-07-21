"""
    Django settings for Guide v1 project.
"""

import os
from datetime import timedelta
from enum import Enum
from pathlib import Path

from django.conf import settings

# pylint: disable=import-error
from helpers.environ.environ import Env  # noqa: F401

# *****************
# *     SETUP     *
# *****************
BASE_DIR = Path(__file__).resolve().parent.parent
env = Env(os.path.join(BASE_DIR.parent, ".env"))
SECRET_KEY = env.str_env("SECRET_KEY")
DEBUG = env.bool_env("DEBUG", 1)
API_BASE_URL = env.str_env("API_BASE_URL")

# **************************
# *     APPLICATIONS       *
# **************************
SHARED_APPS = (
    "daphne",
    # default django apps
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # rest framework
    "rest_framework",
    "django_filters",
    # tenants
    "django_tenants",
    # tenant app
    "services.country",
    # yasg
    "drf_yasg",
    # jwt
    "rest_framework_simplejwt",
    # cors
    "corsheaders",

    # s3
    "storages",
)

TENANT_APPS = (
    "django.contrib.auth",
    "django.contrib.admin",
    # object level permissions
    "guardian",
    # custom apps
    "services.user",
    "services.mailer",
    "django_prometheus",
)

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

# *******************
# *     HOSTS       *
# *******************
ALLOWED_HOSTS = env.list_env("ALLOWED_HOSTS", ",", "*")
CSRF_TRUSTED_ORIGINS = env.list_env(
    "CSRF_TRUSTED_ORIGINS", ",", "http://localhost:8000",
)
CORS_ALLOW_ALL_ORIGINS = env.bool_env("CORS_ALLOW_ALL_ORIGINS", True)
CORS_ALLOW_CREDENTIALS = env.bool_env("CORS_ALLOW_CREDENTIALS", True)

# *******************
# *   MIDDLEWARES   *
# *******************
MIDDLEWARE = [
    # DEBUG
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # CORS
    "corsheaders.middleware.CorsMiddleware",
    # Cache middlewares
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# *******************
# *  DEBUG Configs  *
# *******************
INTERNAL_IPS = [
    "127.0.0.1",
    "0.0.0.0" "localhost",
]

# *******************
# *   URL Configs   *
# *******************
ROOT_URLCONF = "core.urls"
PUBLIC_SCHEMA_URLCONF = "core.shared_urls"

# ********************
# * TEMPLATE Configs *
# ********************
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "services/mailer",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]

# *******************
# * WSGI Configs    *
# *******************
WSGI_APPLICATION = "core.wsgi.application"

# *******************
# * ASGI Configs    *
# *******************
ASGI_APPLICATION = "core.asgi.application"

# *******************
# * DATABASE Config *
# *******************
DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": env.str_env("POSTGRESQL_DATABASE", "postgres"),
        "USER": env.str_env("POSTGRESQL_USER", "postgres"),
        "PASSWORD": env.str_env("POSTGRESQL_PASSWORD", "postgres"),
        "HOST": env.str_env("POSTGRESQL_HOST", "localhost"),
        "PORT": env.str_env("POSTGRESQL_PORT", "5432"),
        "TEST": {
            "NAME": "test_db",
        },
    }
}
DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

# ****************************
# *    PASSWORD Config       *
# ****************************
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ****************************
# *     MODELS Config        *
# ****************************
TENANT_MODEL = "country.Country"
TENANT_DOMAIN_MODEL = "country.Domain"
AUTH_USER_MODEL = "user.User"

# ****************************
# *  INTERNATIONALIZATION    *
# ****************************
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ******************************************
# * STATIC FILES (CSS, JavaScript, Images) *
# ******************************************
FILE_UPLOAD_STORAGE = env.str_env("FILE_UPLOAD_STORAGE", "s3")  # local | s3

match FILE_UPLOAD_STORAGE:
    case "local":
        MEDIA_ROOT_NAME = "media"
        MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_ROOT_NAME)
        MEDIA_URL = f"/{MEDIA_ROOT_NAME}/"
    case "s3":
        DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
        STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
        AWS_S3_ACCESS_KEY_ID = env.str_env("AWS_S3_ACCESS_KEY_ID")
        AWS_S3_SECRET_ACCESS_KEY = env.str_env("AWS_S3_SECRET_ACCESS_KEY")
        AWS_STORAGE_BUCKET_NAME = env.str_env("AWS_STORAGE_BUCKET_NAME")
        AWS_S3_REGION_NAME = env.str_env("AWS_S3_REGION_NAME")
        AWS_S3_SIGNATURE_VERSION = env.str_env("AWS_S3_SIGNATURE_VERSION", "s3v4")
        AWS_DEFAULT_ACL = env.str_env("AWS_DEFAULT_ACL", "public-read")
        AWS_PRESIGNED_EXPIRY = env.int_env("AWS_PRESIGNED_EXPIRY", 10)  # seconds

STATIC_URL = "static/"
STATIC_ROOT = "static"

# ****************************
# *         DEFAULTS         *
# ****************************
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# *****************************
# *          REST API         *
# *****************************
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "helpers.auth.custom_jwt.JWTAuth",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "EXCEPTION_HANDLER": "exceptions_hog.exception_handler",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

# *****************************
# *      AUTHENTICATION       *
# *****************************

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

# ********************************
# *          GUARDIAN            *
# ********************************
ANONYMOUS_USER_NAME = None

# ********************************
# *         EXCEPTIONS           *
# ********************************
EXCEPTIONS_HOG = {
    "EXCEPTION_REPORTING": "exceptions_hog.handler.exception_reporter",
    "ENABLE_IN_DEBUG": False,
    "NESTED_KEY_SEPARATOR": "__",
    "SUPPORT_MULTIPLE_EXCEPTIONS": False,
}

# ********************************
# *              JWT             *
# ********************************
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,  # TODO change to your domain ! get from env !
    "ISSUER": None,  # TODO change to your domain ! get from env !
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "id",
    "USER_AUTHENTICATION_RULE": "helpers.auth.custom_jwt.custom_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=20),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    # customized settings
    "COUNTRY_ID_FIELD": "id",
    "COUNTRY_ID_CLAIM": "id",
    "ACTIVATION_TOKEN_LIFETIME": timedelta(hours=1),
    "VERIFICATION_TOKEN_LIFETIME": timedelta(days=7),
    "COUNTRY_MODEL": "country.Country",
    "USER_MODEL": "users.User",
}

# *************************************
# *          SWAGGER                  *
# *************************************
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

# *******************************
# *         EMAIL               *
# *******************************
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST_PASSWORD = env.str_env("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = env.str_env("EMAIL_HOST_USER")
EMAIL_USE_TLS = env.bool_env("EMAIL_USE_TLS", 1)
EMAIL_USE_SSL = env.bool_env("EMAIL_USE_SSL", 0)
EMAIL_HOST = env.str_env("EMAIL_HOST")
EMAIL_PORT = env.str_env("EMAIL_PORT")
EMAIL_FROM = env.str_env("EMAIL_FROM")

# *******************************
# *         REDIS               *
# *******************************
REDIS_HOST = env.str_env("REDIS_HOST")
REDIS_PORT = env.str_env("REDIS_PORT")
REDIS_PASSWORD = env.str_env("REDIS_PASSWORD")
REDIS_DB = env.str_env("REDIS_DB")
DJANGO_CACHING_REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/10"

# *******************************
# *         MONITORING          *
# *******************************
PROMETHEUS_EXPORT_MIGRATIONS = (
    False  # very important, otherwise `makemigrations` command will fail
)

# *******************************
# *         CLIENT              *
# *******************************
CLIENT_URL = env.str_env("CLIENT_URL", "http://localhost:3000")
SHOW_PUBLIC_IF_NO_TENANT_FOUND = env.bool_env("SHOW_PUBLIC_IF_NO_TENANT_FOUND", 1)

# *******************************
# *          CACHE              *
# *******************************
# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": DJANGO_CACHING_REDIS_URL,
#     }
# }
CACHE_MIDDLEWARE_ALIAS = "default"
CACHE_MIDDLEWARE_SECONDS = 5
CACHE_MIDDLEWARE_KEY_PREFIX = "django-site-cache"

# *******************************
# *       REGISTRATION          *
# *******************************
BLACK_LIST_DOMAINS = env.list_env("BLACK_LIST_DOMAINS", ",", "")
ALLOWED_EMAIL_DOMAINS = env.list_env("ALLOWED_EMAIL_DOMAINS", ",", "")
VALID_DOMAINS_REGEX = env.str_env(
    "VALID_DOMAINS_REGEX",
    "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*"
    "[a-zA-Z0-9])\.)*([A-Za-z0-9]|"
    "[A-Za-z0-9][A-Za-z0-9\-]*"
    "[A-Za-z0-9])$",
)

APP_DOMAIN = env.str_env("APP_DOMAIN", "http://localhost")

# *******************************
# *          Channels           *
# *******************************
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"],
        },
    }
}

FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024 * 1024  # 5GB
DATA_UPLOAD_MAX_NUMBER_FILES = 1000000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000000
