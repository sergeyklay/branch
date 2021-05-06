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

"""SEO related template tags."""

import unicodedata
from html import unescape

from bs4 import BeautifulSoup
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def sanitize_description(raw_text):
    """Sanitize website description."""

    unescaped = unescape(raw_text or '')
    normalized = unicodedata.normalize('NFKC', unescaped)

    soup = BeautifulSoup(normalized, features='html.parser')

    # Strip HTML tags
    quoted = soup.get_text()

    # Any time quotation marks are used in the HTML of a meta description,
    # Google cuts off that description at the quotation mark when it appears
    # on a SERP.
    unquoted = quoted \
        .replace("'", '') \
        .replace('"', '') \
        .replace('“', '') \
        .replace('”', '') \
        .replace('’', '') \
        .replace('‘', '')

    # Search engines generally truncates snippets to ~155–160 characters.
    return unquoted[0:155]
