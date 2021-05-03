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

"""Development Django settings for branch project."""

from django.contrib.messages import constants as message_constants

# pylint: disable-msg=w0614,w0401
from .base import *  # noqa

# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG = True

MESSAGE_LEVEL = message_constants.DEBUG

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',  # Debug Toolbar
    'django_extensions',  # A collection of custom extensions for the Django
)

MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE

# SECURITY WARNING: define the correct hosts in production
ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '[::1]']

INTERNAL_IPS = ['.localhost', '127.0.0.1', '[::1]']

COMPRESS_OFFLINE = env.bool('COMPRESS_OFFLINE', False)

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Caches
CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
