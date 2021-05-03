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

"""Testing Django settings for branch project."""

# pylint: disable-msg=w0614,w0401
from .base import *  # noqa

# SECURITY WARNING: define the correct hosts in production
ALLOWED_HOSTS = ('.localhost', '127.0.0.1', '[::1]')

INTERNAL_IPS = ('.localhost', '127.0.0.1', '[::1]')

SECRET_KEY = 'Naive and not very secret key used for tests'

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Caches
CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
