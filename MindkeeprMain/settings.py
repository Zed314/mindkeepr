"""
Django settings for MindkeeprMain project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = int(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'mozilla_django_oidc',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'polymorphic',
    'taggit',
    'crispy_forms',
    'Mindkeepr',
    'django_cleanup',
    "django_select2",
    "corsheaders"
]


CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'corsheaders.middleware.CorsMiddleware'
]

#TODO : for react, MUST BE CHANGED LATERRR
ALLOWED_HOSTS=['*']

CORS_ORIGIN_ALLOW_ALL = True


#ALLOWED_HOSTS=['http://127.0.0.1:3001']
#
#CORS_ORIGIN_ALLOW_ALL = False
#
#
#CORS_ORIGIN_WHITELIST = (
#       'http://127.0.0.1:3001',
#
#)



OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 180

ROOT_URLCONF = 'MindkeeprMain.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MindkeeprMain.wsgi.application'

REST_FRAMEWORK = {
    #todo : temp
    'DEFAULT_PERMISSION_CLASSES': [
       # 'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework_datatables.pagination.DatatablesPageNumberPagination',
    'PAGE_SIZE': 50,
}

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


#sqlite = {'ENGINE': 'django.db.backends.sqlite3', 'NAME': os.path.join(BASE_DIR, 'db.sqlite3')}
#postgres = {'ENGINE': 'django.db.backends.postgresql',
#            'NAME': 'postgres',
#            'USER': 'postgres',
#            'HOST': 'db',
#            'PORT': 5432,
#            }
if not 'test' in sys.argv and not 'test_coverage' in sys.argv:
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        'MindkeeprMain.auth.MyOIDCAB',
        # ...
    )
else:
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',
        # ...
    )

if not 'test' in sys.argv and not 'test_coverage' in sys.argv:

    OIDC_RP_CLIENT_SECRET = "TBD"
    OIDC_RP_IDP_SIGN_KEY = "TBD"
    OIDC_RP_CLIENT_ID = "mindkeepr"
    OIDC_OP_AUTHORIZATION_ENDPOINT = "TBD"
    OIDC_OP_TOKEN_ENDPOINT = "TBD/auth/realms/master/protocol/openid-connect/token"
    OIDC_OP_USER_ENDPOINT =  "TBD/auth/realms/master/protocol/openid-connect/userinfo"
    OIDC_RP_SIGN_ALGO="RS256"
    OIDC_OP_JWKS_ENDPOINT = "TBD/auth/realms/master/protocol/openid-connect/certs"






# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

"""
TODO : add default and enable cache
# Cache-cache
CACHES = {

    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Tell select2 which cache configuration to use:
SELECT2_CACHE_BACKEND = "select2"
"""

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_REDIRECT_URL="/"
LOGOUT_REDIRECT_URL="/"

if os.environ.get("DEV"):
    from MindkeeprMain.dev import *
else:
    from MindkeeprMain.prod import *

if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    print("Test database : sqlite3",flush="true")
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'