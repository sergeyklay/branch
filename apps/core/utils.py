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

"""Common utils for the whole project."""

from django.conf import settings

from branch.settings.base import env


def is_prod_like_environment():
    """Is the current environment is production-like?"""
    if settings.DEBUG:
        return False

    prod_like = [f'branch.settings.{e}' for e in ['prod', 'staging']]
    return env.str('DJANGO_SETTINGS_MODULE') in prod_like


def admin_path():
    """Get URL part of the admin site."""
    admin = getattr(settings, 'ADMIN_SITE_URL', 'admin')
    return f"{admin.strip('/')}"
