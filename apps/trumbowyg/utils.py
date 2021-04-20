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

"""Common utils for the trumbowyg application."""

import unicodedata
from html import unescape

from bs4 import BeautifulSoup as bs

REMOVABLE_TAGS = (
    'script', 'style',
)

ALLOWED_TAGS = (
    'ul', 'ol', 'li', 'strong', 'em', 'del',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'br', 'hr',
)

ALLOWED_ATTRS = (
    'href', 'src', 'alt', 'width', 'height',
    'style', 'target', 'rel',
)


def content_sanitize(raw_text, allowed_tags=None, allowed_attrs=None,
                     unescape_tags=True, prettify=True):
    """
    Sanitize given text.

    This function does the following sanitize actions:
    - Remove escaped html characters
    - Convert weird quote chars and use standard chars instead
    - Normalize unicode characters
    - Remove all `script` html tags
    - Strip most of html tags
    - Removes all html tag attributes
    - Autoindent existing html
    """

    allowed_tags = ALLOWED_TAGS + allowed_tags or ()
    allowed_attrs = ALLOWED_ATTRS + allowed_attrs or ()

    if unescape_tags:
        # This will convert all named and numeric character references
        # in the raw_text to the corresponding Unicode characters:
        #    <code>&lt;h1&gt;</code> -> <code><h1></code>
        unescaped = unescape(raw_text or '')
    else:
        # This allows use something like
        #    <code>&lt;h1&gt;</code>
        # in the posts
        unescaped = raw_text or ''

    unquoted = unescaped \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'") \
        .replace('target="_blank"', 'target="_blank" rel="noopener"')

    normalized = unicodedata.normalize('NFKC', unquoted)

    soup = bs(normalized, features='html.parser')
    tags = soup.find_all()

    for tag in tags:
        if tag.name in REMOVABLE_TAGS or not tag.name:
            tag.decompose()
        else:
            if tag.name in allowed_tags:
                attrs = list(tag.attrs.keys())
                for attr in attrs:
                    if attr not in allowed_attrs:
                        tag.attrs.pop(attr)
                if not tag.contents and tag.name not in ['br', 'img']:
                    tag.decompose()
                elif tag.string and not tag.string.strip():
                    tag.decompose()
            else:
                tag.unwrap()

    if prettify:
        # Autoindent html code
        return soup.prettify()

    # Return just a string, with no fancy formatting
    return str(soup)
