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

"""Query parameters template tag."""

from urllib.parse import quote, urlencode

from django import template

register = template.Library()


@register.simple_tag
def urlparams(*_, **kwargs):
    """
    Query parameters template tag.

    Usage:
      {% load urlparams %}
      {% url 'blog:post_list' %}{% urlparams page=page.previous_page_number %}
    """
    safe_args = {k: v for k, v in kwargs.items() if v is not None}
    return f'?{urlencode(safe_args, quote_via=quote)}' if safe_args else ''
