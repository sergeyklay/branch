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

"""Telegraph application module."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TelegraphConfig(AppConfig):
    """Class representing telegraph application and its configuration."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.telegraph'
    verbose_name = _('Telegraph')
