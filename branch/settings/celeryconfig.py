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

"""Celery configuration module."""

from django.conf import settings

from .base import env

# Default broker URL.
broker_url = env.str('BROKER_URL', default=None)

# The backend used to store task state and results (tombstones).
result_backend = env.str('CELERY_RESULT_BACKEND', default=None)

# If this is True, all tasks will be executed locally by blocking until the
# task returns.
#
# Useful for local development, testing and debugging.
task_always_eager = settings.DEBUG
if env.str('DJANGO_SETTINGS_MODULE') == 'branch.settings.test':
    task_always_eager = True

# If this is True, eagerly executed tasks (applied by task.apply(), or when the
# task_always_eager setting is enabled), will propagate exceptions.
# Good for sanity.
#
# Useful for local development, testing and debugging.
task_eager_propagates = task_always_eager

# Number of CPU cores.
worker_concurrency = env.int('CELERYD_CONCURRENCY', default=1)

# Name of the pool class used by the worker.
worker_pool = env.str('CELERYD_POOL', default='prefork')

# Configure Celery to use a custom time zone.
timezone = env.bool('CELERY_TIMEZONE', default=settings.TIME_ZONE)

# The default timeout in seconds before we give up establishing a
# connection to the AMQP server.
broker_connection_timeout = env.float('BROKER_CONNECTION_TIMEOUT', default=4.0)

# Toggles SSL usage on broker connection and SSL settings.
broker_use_ssl = None

# The Redis backend supports SSL.
redis_backend_use_ssl = None

if env.bool('CELERY_USE_SSL', default=False):
    import ssl

    _ssl_conf = {
        'ssl_cert_reqs': ssl.CERT_NONE,
        'ssl_ca_certs': None,
        'ssl_certfile': None,
        'ssl_keyfile': None,
    }

    broker_use_ssl = _ssl_conf
    redis_backend_use_ssl = _ssl_conf
