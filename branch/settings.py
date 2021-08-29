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
Django settings  for branch project.

Generated by 'django-admin startproject' using Django 3.2rc1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import logging
import os
import re
import socket
import sys
import warnings
from datetime import datetime
from pathlib import Path

from django.contrib.messages import constants as message_constants
from django.utils.translation import gettext_lazy as _
from environ import environ  # noqa

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Set VAR=(casting, default value)
env = environ.Env(
    DEBUG=(bool, False),
    ALLOW_ROBOTS=(bool, False),
    USE_SSL=(bool, False),
    COMPRESS_OFFLINE=(bool, False),
    ALLOWED_HOSTS=(list, []),
    INTERNAL_IPS=(list, []),
    ADMINS=(list, []),
    TIME_ZONE=(str, 'UTC'),
    SECURE_SSL_REDIRECT=(bool, False),
    SECURE_HSTS_SECONDS=(int, 3600),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, False),
    SECURE_HSTS_PRELOAD=(bool, False),
    SESSION_COOKIE_SECURE=(bool, False),
    CSRF_COOKIE_SECURE=(bool, False),

    # Celery
    CELERY_ALWAYS_EAGER=(bool, True),
    CELERY_USE_SSL=(bool, False),
    CELERY_RESULT_BACKEND=(str, None),
    CELERYD_CONCURRENCY=(int, 1),
    CELERYD_POOL=(str, 'prefork'),
    BROKER_URL=(str, None),
    BROKER_CONNECTION_TIMEOUT=(float, 4.0),
)

# Reading environment file.
if os.path.exists(BASE_DIR / '.env'):
    env.read_env(BASE_DIR / '.env')

APPS_DIR = BASE_DIR / 'apps'
sys.path.append(APPS_DIR.__str__())

# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG = env('DEBUG')

if DEBUG:
    # Always issue warnings messages in debug mode for the following classes:
    warnings.simplefilter('always', DeprecationWarning)
    warnings.simplefilter('always', PendingDeprecationWarning)

try:
    # If it is possible to import and grab BUILD_ID_SHORT store first four
    # chars to add later to CACHE_KEY_PREFIX. BUILD_DATE_SHORT will be used
    # in robots.txt
    from build import BUILD_ID_SHORT, BUILD_DATE_SHORT  # pylint: disable=W0611
except ImportError:
    BUILD_ID_SHORT = '0000'
    BUILD_DATE_SHORT = datetime.utcnow().strftime('%Y-%m-%d')

# Minimum message recorded level.
# https://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-levels
MESSAGE_LEVEL = message_constants.DEBUG if DEBUG else message_constants.INFO

# The host currently running the site.
HOSTNAME = socket.gethostname()  # pylint: disable=E1101

# The front end domain of the site.
DOMAIN = env.str('DOMAIN', default=HOSTNAME)

# Full base URL for the site including protocol.  No trailing slash.
#   Example: https://my-site.com
USE_SSL = env('USE_SSL')
SITE_URL = f"{'https' if USE_SSL else 'http'}://{DOMAIN}"

# SECURITY WARNING: define the correct hosts and ips in production
ALLOWED_HOSTS = env('ALLOWED_HOSTS')
INTERNAL_IPS = env('INTERNAL_IPS')

# Should robots.txt allow everything to be crawled?
ALLOW_ROBOTS = env('ALLOW_ROBOTS')

# List of compiled regular expression objects representing URLs that need not
# be reported by BrokenLinkEmailsMiddleware.
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

# SECURITY WARNING: keep the secret key used in production secret!
# Raises django's ImproperlyConfigured exception if SECRET_KEY
# is not in os.environ
SECRET_KEY = env.str('SECRET_KEY')


# Application definition

DJANGO_APPS = [
    # Default Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    # Admin
    'django.contrib.admin',
]

THIRD_PARTY_APPS = [
    'captcha',  # reCAPTCHA support for Django.
    'compressor',  # Compress JS and CSS into single cached file.
]

if DEBUG:
    THIRD_PARTY_APPS += [
        'debug_toolbar',
        'django_extensions',
    ]

# Apps specific for this project go here.
LOCAL_APPS = [
    'apps.core',
    'apps.seo',
    'apps.trumbowyg',
    'apps.blog',
    'apps.telegraph',
    'apps.pages',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Caches

# Prefix for cache keys (will prevent collisions when running parallel copies)
CACHE_KEY_PREFIX = f'branch:{BUILD_ID_SHORT}:'

CACHES = {
    'default': env.cache(
        default='dummycache:',
        backend=env.str('CACHE_BACKEND', None)
    )
}

CACHES['default']['TIMEOUT'] = 500
CACHES['default']['KEY_PREFIX'] = CACHE_KEY_PREFIX

CACHE_MIDDLEWARE_KEY_PREFIX = CACHE_KEY_PREFIX

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

if DEBUG:
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'branch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'apps.core.context_processors.base_url',
                'apps.core.context_processors.i18n',
                'apps.core.context_processors.global_settings',

                'apps.seo.context_processors.google_analytics',

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
    """Get Database configuration."""
    values = env.db(var=environ_var, default='sqlite:///storage/db/db.sqlite3')

    def is_sqlite(options: dict):
        return options.get('ENGINE') == 'django.db.backends.sqlite3'

    values.update(
        {
            # Pool our database connections up for 60 seconds.
            # This is almost irrelevant for SQLite, so check this first.
            'CONN_MAX_AGE': 0 if is_sqlite(values) else 60,
        }
    )

    if not is_sqlite(values):
        return values

    # This will allow use a relative DB path for SQLite
    # like 'sqlite:///storage/db/db.sqlite3'
    if not values['NAME'] == ':memory:' and not os.path.isabs(values['NAME']):
        values.update({'NAME': BASE_DIR / values['NAME']})

    return values


DATABASES = {
    'default': get_db_config('DATABASE_URL'),
}

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console_dev', 'console_prod', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console_dev', 'console_prod', 'file'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['console_dev'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.template': {
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
        'file': {
            'class': 'logging.FileHandler',
            'filename': env.str('LOG_FILE', BASE_DIR / 'storage/logs/app.log'),
            'level': 'INFO',
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

logging.captureWarnings(True)

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
    BASE_DIR / 'fixtures',
)

ADMIN_SITE_URL = env.str('ADMIN_SITE_URL', default='admin/')

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

BRANCH_LANGUAGES = {
    'en-US': {
        'english': 'English (US)',
        'native': 'English (US)',
        'region': 'en_US',
    },
    'ru': {
        'english': 'Russian',
        'native': '\u0420\u0443\u0441\u0441\u043a\u0438\u0439',
        'region': 'ru_RU',
    },
    'uk': {
        'english': 'Ukrainian',
        'native': '\u0423\u043a\u0440\u0430\u0457\u043d\u0441\u044c\u043a\u0430',  # noqa
        'region': 'uk_UA',
    },
}

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html

LANGUAGE_CODE = 'en-us'

LANGUAGE_COOKIE_NAME = 'branch_language'
LANGUAGES = [
    (locale.lower(), value['native']) for locale, value in BRANCH_LANGUAGES.items()  # noqa
]

LANGUAGE_MAP = {locale.lower(): locale for locale in BRANCH_LANGUAGES}
LOCALE_TERRITORY = [
    (locale['region'], locale['native']) for locale in BRANCH_LANGUAGES.values() # noqa
]

TIME_ZONE = env('TIME_ZONE')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locales',
]

NODE_MODULES_PATH = BASE_DIR / 'node_modules'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = (
    BASE_DIR / 'assets',
    NODE_MODULES_PATH,
    BASE_DIR.joinpath('apps', 'blog', 'assets'),
    BASE_DIR.joinpath('apps', 'seo', 'assets'),
    BASE_DIR.joinpath('apps', 'trumbowyg', 'assets'),
    BASE_DIR.joinpath('apps', 'telegraph', 'assets'),
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
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/dev/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Project configuration

SITE_NAME = _('Serghei Iakovlev')
SITE_DESCRIPTION = _("Serghei's Iakovlev Blog")
SITE_TAGLINE = _('My notebook, workshop, a place where I share my '
                 'experiences and thoughts')

COPYRIGHT_HOLDER = SITE_NAME
GITHUB_USER = 'sergeyklay'

PAGE_SIZE = 5

# red, orange, magenta, cyan, blue, brown
COLOR_SCHEME = ''

# Email configuration

# The email address that error messages come from
SERVER_EMAIL = env.str('SERVER_EMAIL', default='webmaster@localhost')
EMAIL_CONFIG = env.email_url(backend=env.str('EMAIL_BACKEND', default=None))
vars().update(EMAIL_CONFIG)

# The email address that website messages come to
CONTACT_EMAIL = env.str('CONTACT_EMAIL', default='webmaster@localhost')

DEFAULT_FROM_EMAIL = SERVER_EMAIL

# A list of all the people who get code error notifications.
#
# Convert ['name1:email1', 'name2:email2'] to
# [('name1', 'email1'), ('name2', 'email2')]
ADMINS = [tuple(admin.split(':')) for admin in env.list('ADMINS')]

# Redirect all non-HTTPS requests to HTTPS (except for those URLs matching a
# regular expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT')

# Add the 'includeSubDomains' directive to the HTTP Strict Transport Security
# header.
SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')

# Add the 'includeSubDomains' directive to the HTTP Strict Transport Security
# header.
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS')

# Add the 'preload' directive to the HTTP Strict Transport Security header.
SECURE_HSTS_PRELOAD = env('SECURE_HSTS_PRELOAD')

# Whether to use a secure cookie for the session cookie. If this is set to
# True, the cookie will be marked as “secure”, which means browsers may ensure
# that the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE')

# Whether to use a secure cookie for the CSRF cookie. If this is set to True,
# the cookie will be marked as “secure”, which means browsers may ensure that
# the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE')

# Syndication

FEED_MAX_ITEMS = 20
FEED_WORD_LIMIT = 50

# SEO Tools

GA_TRACKING_ID = env.str('GA_TRACKING_ID', default='')
# Do not translate this
SEO_KEYWORDS = ('язык программирования, грамматики, грамматика, компиляторы, '
                'парсеры, сканеры')

# reCAPTCHA

RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY', default='')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY', default='')
RECAPTCHA_REQUIRED_SCORE = 0.75
