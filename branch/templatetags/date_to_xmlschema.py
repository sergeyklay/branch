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

"""Date to XML Schema filter."""

from datetime import datetime

from django import template

register = template.Library()


@register.filter(expects_localtime=True, is_safe=False)
def date_to_xmlschema(value):
    """
    Format a date according to the ISO 8601 format.

    Usage:
      {% date_to_xmlschema %}
      {{ post.published_at|date_to_xmlschema }}

    For more see: https://www.iso.org/standard/70907.html
    """
    if not isinstance(value, datetime):
        return ''

    return value.replace(microsecond=0).isoformat()
