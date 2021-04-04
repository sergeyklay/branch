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
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[
    '127.0.0.1',
    '.blog.local',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',
    '.ngrok.io',
])

INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])
