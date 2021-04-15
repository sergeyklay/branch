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

# Website base url
BASE_URL = env.str('BASE_URL', default='http://127.0.0.1')

# Application definition

# The database ID of the django.contrib.sites.models.Site
# object associated with that particular settings file.
SITE_ID = 1

DJANGO_APPS = (
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Sitemap requirements
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Admin
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'compressor',  # Compress JS and CSS into single cached file.
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'apps.website',
    'apps.blog',
    'apps.telegraph',
    'apps.pages',
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

    'apps.website.middleware.locale.inject_accept_language',
    'django.middleware.locale.LocaleMiddleware',
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

                'apps.website.context_processors.locale',
                'apps.website.context_processors.app_settings',
                'apps.website.context_processors.base_url',

                'apps.pages.context_processors.pages',
            ],
            'libraries': {
                'urlparams': 'branch.templatetags.urlparams',
                'date_to_xmlschema': 'branch.templatetags.date_to_xmlschema',
            },
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

#  Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console_dev', 'console_prod'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console_dev', 'console_prod'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['console_dev'],
            'propagate': True,
            'level': 'INFO',
        },
    },
    'handlers': {
        'console_dev': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'common',
            'filters': ['require_debug_true'],
        },
        'console_prod': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'common',
            'filters': ['require_debug_false'],
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'common': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
    },
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

FIXTURE_DIRS = (
    BASE_DIR('provision', 'fixtures'),
)

ADMIN_SITE_URL = env.str('ADMIN_SITE_URL', default='admin/')

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

ADMIN_LANGUAGE_CODE = 'ru'
DEFAULT_LANGUAGE_CODE = 'ru'

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

COMMON_ASSETS_PATH = BASE_DIR('assets')
NODE_MODULES_PATH = BASE_DIR('node_modules')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('static')
STATICFILES_DIRS = (
    COMMON_ASSETS_PATH,
    NODE_MODULES_PATH,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_OUTPUT_DIR = ''  # Compress to '/static/{css,js}/'
COMPRESS_PRECOMPILERS = (
    (
        'text/x-scss',
        'sass -I {} --no-source-map {{infile}} {{outfile}}'.format(
            NODE_MODULES_PATH,
        )
    ),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR('media')

# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email configuration

EMAIL_HOST = env.str('EMAIL_HOST', default='localhost')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=25)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=EMAIL_HOST != 'localhost')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Syndication

FEED_MAX_ITEMS = 20
FEED_WORD_LIMIT = 30
