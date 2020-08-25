"""Django 2.2.2"""
from __future__ import absolute_import, unicode_literals
from django.utils.translation import ugettext_lazy as _
import os, environ
from datetime import timedelta


ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path('main')
CONF_DIR = ROOT_DIR.path('config')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
env.read_env('.env')

SECRET_KEY = env("SECRET_KEY", default='8na#(#x@0i*3ah%&$-q)b&wqu5ct_a3))d8-sqk-ux*5lol*wl')

DEBUG = env.bool("DEBUG", False)

SITE_ID = int(env("SITE_ID", default='1'))

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'crequest',
    'channels',
    'rest_framework',
    'django_extensions',
    'crispy_forms',
    'main.api',
    'main.core',
    'main.notify',
    'main.order',
    'main.taskapp',
    'main.users',
    'main.web',
    'main.reseller',
    'main.yemekkalmasin_log',
    'main.tickets',
    'widget_tweaks',
    'django_countries',
    'djoser',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_auth.registration',
    'rest_framework.authtoken',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crequest.middleware.CrequestMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path('templates')),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.core.context_processors.site',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

WSGI_APPLICATION = 'config.wsgi.application'

ROOT_URLCONF = 'config.urls'

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),)

LOGIN_URL = "/user/login/"

RESELLER_URL = env('RESELLER_URL', default="reseller/")

ADMIN_URL = env('ADMIN_URL', default="admin/")

LOCALE_PATHS = (str(APPS_DIR('locale')), str(CONF_DIR('locale')),)

LANGUAGE_CODE = env('LANGUAGE_CODE', default="en")

LANGUAGES = (
    ('en', _('English')),
    ('tr', _('Türkçe')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_TITLE  = "YK site admin"
SITE_HEADER = "YK administration"
INDEX_TITLE = "Dashboard administration"

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'info',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

STATIC_ROOT = str(ROOT_DIR('public/static'))

STATIC_URL = '/static/'

STATICFILES_DIRS = (str(APPS_DIR.path('static',)),)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = str(ROOT_DIR('public/media'))

MEDIA_URL = '/media/'

REDIS_URL = ('localhost', 6379) #env.str('REDIS_URL', default=('localhost', 6379))
ASGI_APPLICATION = "config.routing.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL,],
        },
    },
}
THIRD_PARTY_APPS = (
    'widget_tweaks',
)

DEFAULT_USER_AVATAR = MEDIA_URL + "users/user.png"
DEFAULT_USER_FOLDER = "users"

DEFAULT_COMPANY_LOGO   = MEDIA_URL + "companies/company.png"
DEFAULT_COMPANY_FOLDER = "companies"

DEFAULT_PRODUCT_IMAGE  = MEDIA_URL + "products/product.png"
DEFAULT_PRODUCT_FOLDER = "products"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_THROTTLE_RATES' : {
        'registerthrottle' : '105/hour',
    }
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME'  : timedelta(minutes=15)
}

DISPLAY_API_ROOT = env.bool("DISPLAY_API_ROOT", default=True)
DEFAULT_CITY_NAME = env("DEFAULT_CITY_NAME", default="Istanbul")
DEFAULT_COUNTRY_CODE = env("DEFAULT_COUNTRY_CODE", default="TR")

HOST_SCHEMA = env('HOST_SCHEMA', default="http://")
DOMAIN_NAME = env('DOMAIN_NAME', default="localhost")


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  
MAILER_EMAIL_BACKEND = EMAIL_BACKEND  
EMAIL_HOST = 'smtp.yandex.com'  
EMAIL_HOST_PASSWORD = 'aqjbitmvdglitraq'  
EMAIL_HOST_USER = 'info@yemekkalmasin.com'  
EMAIL_PORT = 465  
EMAIL_USE_SSL = True  
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CKEDITOR_UPLOAD_PATH = MEDIA_URL + "ckeditor/images/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}