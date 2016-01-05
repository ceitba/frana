# coding: utf-8
"""
Django settings for ceitba project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""
from __future__ import unicode_literals
import os

import dj_database_url
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd-u2-!18(xgc3s-_s40e_1c_bx@+2z(wjpz2q1c^=d*ht!y*y!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

LOGIN_URL = reverse_lazy('bookings:login')

LOGIN_REDIRECT_URL = reverse_lazy('bookings:index')

DATE_FORMAT = 'd/m/Y'

DATE_INPUT_FORMATS = ['%d/%m/%Y']

DATETIME_INPUT_FORMATS = ['%d/%m/%Y']

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'bootstrap3',
    'constance',
    'constance.backends.database',
    'django_extensions',
    # 'pipeline',

    # Own apps
    'bookings',
]

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar'
    ]


MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ceitba.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'ceitba.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default='sqlite:///db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ar'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}


# Messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}


# Constance

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'WEEKDAY_PRICE': (40, 'Precio para los días de semana'),
    'WEEKEND_PRICE': (80, 'Precio para los fines de semana'),
    'BOOKING_DISABLED': (False, 'Deshabilitar reservas'),
    'BOOKING_DISABLED_CAUSE': ('', 'Causa por la cual están deshabilitadas las reservas'),
    'BOOKING_DAYS_FUTURE': (14, 'Cantidad de días a futuro que se pueden realizar las reservas'),
}


# Pipeline

PIPELINE = {
    'PIPELINE_ENABLED': False,
    'STYLESHEETS': {
        'styles': {
            'source_filenames': [
                'js/jquery.js',
                'js/d3.js',
                'js/collections/*.js',
                'js/application.js',
            ],
            'output_filename': 'js/stats.js',
        }
    },
    'COMPILERS': {
        'pipeline.compilers.sass.SASSCompiler',
    }
}


# Bootstrap

BOOTSTRAP3 = {
    'field_renderers': {
        'default': 'bookings.fields.FieldRenderer'
    }
}
