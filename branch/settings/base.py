# Copyright (C) 2021 Serghei Iakovlev <egrep@protonmail.ch>
#
# This file is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <https://www.gnu.org/licenses/>.

"""
Base Django settings for branch project.

Generated by 'django-admin startproject' using Django 3.2rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os
import sys

import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR('subdir').
BASE_DIR = environ.Path(__file__) - 3

env = environ.Env()

# Reading environment file.
# OS environment variables take precedence over variables from environment file
ENVIRON_SETTINGS_FILE_PATH = BASE_DIR('settings.env')
if os.path.exists(ENVIRON_SETTINGS_FILE_PATH):
    env.read_env(ENVIRON_SETTINGS_FILE_PATH)

APPS_DIR = BASE_DIR('apps')
sys.path.append(APPS_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY
# is not in os.environ
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG = False

# SECURITY WARNING: define the correct hosts in production
ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = (
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Admin
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    # Compress JS and CSS into single cached file.
    'compressor',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.blog',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'branch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'branch.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases


def get_db_config(environ_var):
    """Get Database configuration"""
    values = env.db(var=environ_var, default='sqlite:///db.sqlite3')

    def is_sqlite(options):
        return options['ENGINE'] == 'django.db.backends.sqlite3'

    def is_relative(name):
        return not os.path.isabs(name)

    values.update(
        {
            # Pool our database connections up for 60 seconds.
            # This is almost irrelevant for SQLite, so check this first.
            'CONN_MAX_AGE': 0 if is_sqlite(values) else 60,
        }
    )

    # This will allow use a relative DB path for SQLite
    # like 'sqlite:///db.sqlite3'
    if is_sqlite(values) and is_relative(values['NAME']):
        values.update({'NAME': BASE_DIR(values['NAME'])})

    return values


DATABASES = {
    'default': get_db_config('DATABASE_URL'),
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

VALIDATORS_PATH = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{VALIDATORS_PATH}.UserAttributeSimilarityValidator'},
    {'NAME': f'{VALIDATORS_PATH}.MinimumLengthValidator'},
    {'NAME': f'{VALIDATORS_PATH}.CommonPasswordValidator'},
    {'NAME': f'{VALIDATORS_PATH}.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'branch_language'
LANGUAGES = (
    ('en-us', _('English')),
    ('uk', _('Ukrainian')),
    ('ru', _('Russian')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR('locales'),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

COMMON_ASSETS = BASE_DIR('assets')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('static')
STATICFILES_DIRS = (
    COMMON_ASSETS,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

SASS_PATH = 'make css'

COMPRESS_OUTPUT_DIR = 'compiled'
COMPRESS_PRECOMPILERS = (
    (
        'text/x-scss',
        '{} include={} infile={{infile}} outfile={{outfile}}'.format(
            SASS_PATH,
            COMMON_ASSETS,
        )
    ),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR('media')

# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
