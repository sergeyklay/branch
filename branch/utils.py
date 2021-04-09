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

from html import unescape
from unicodedata import normalize

from bs4 import BeautifulSoup as bs
from django.conf import settings

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


def highlight_js():
    """Perform manipulation of asset paths to enable highlight."""
    components = (
        'abnf', 'antlr4', 'apacheconf',
        'bash', 'bison', 'bnf',
        'c', 'cpp',
        'diff',
        'ebnf',
        'python',
    )

    trumbowyg_plugins = 'trumbowyg/dist/plugins'
    prefix = 'prismjs/components/prism'
    suffix = f"{'' if settings.DEBUG else '.min'}"

    trumbowyg_base = f'{trumbowyg_plugins}/highlight/trumbowyg.highlight'
    trumbowyg = f"{trumbowyg_base}{'' if settings.DEBUG else '.min'}.js"

    result = map(lambda c: f'{prefix}-{c}{suffix}.js', components)
    return ['prismjs/prism.js'] + list(result) + [trumbowyg]


def content_sanitize(raw_text, allowed_tags=None, allowed_attrs=None):
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

    unescaped = unescape(raw_text or '')

    unquoted = unescaped \
        .replace('“', '"') \
        .replace('”', '"') \
        .replace('’', "'") \
        .replace('target="_blank"', 'target="_blank" rel="noopener"')

    normalized = normalize('NFKC', unquoted)

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

    return soup.prettify()


def admin_path():
    """Get URL part of the admin site."""
    admin = getattr(settings, 'ADMIN_SITE_URL', 'admin')
    return f"{admin.strip('/')}"


class RichTextAdminMedia:
    """
    Rich text metadata class to use for posts and pages.

    Setup static assets to use in WYSIWYG editor.
    """

    _suffix = '' if settings.DEBUG else '.min'
    _tw_dist = 'trumbowyg/dist'
    _tw_plugins = f'{_tw_dist}/plugins'

    css = {
        'all': (
            'prismjs/themes/prism.css',
            f'{_tw_dist}/ui/trumbowyg{_suffix}.css',
            f'{_tw_plugins}/highlight/ui/trumbowyg.highlight{_suffix}.css',
        ),
    }

    js = [
        'admin/js/jquery.init.js',
        'js/shared.js',
        f'{_tw_dist}/trumbowyg{_suffix}.js',
        f'{_tw_plugins}/upload/trumbowyg.upload{_suffix}.js',
        'admin/js/richtext.editor.js',
    ] + highlight_js()
