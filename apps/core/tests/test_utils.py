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

import pytest
from django.conf import settings

from apps.core.utils import to_absolute_url, to_language


@pytest.mark.parametrize(
    'locale,expected',
    [
        ('en_US', 'en-US'),
        ('ru_RU', 'ru-RU'),
        ('uk_UA', 'uk-UA'),
        ('en', 'en'),
        ('', ''),
        ('fr-fr', 'fr-FR'),
    ]
)
def test_to_language(locale, expected):
    """Make sure we correct transform locale to language."""
    assert to_language(locale) == expected


@pytest.mark.parametrize(
    'url,site,expected',
    [
        ('', None, settings.BASE_URL),
        ('', '', settings.BASE_URL),
        (None, None, settings.BASE_URL),
        ('foo', None, f'{settings.BASE_URL}/foo'),
        ('http://abc', None, 'http://abc'),
        ('https://cde', None, 'https://cde'),
        ('https://example.com', 'https://foo.com', 'https://example.com'),
        ('woo', 'www', 'woo'),
        ('foobar', 'https://site.com', 'https://site.com/foobar'),
        ('mailto:a@b.c', 'https://site.com', 'mailto:a@b.c'),
    ]
)
def test_to_absolute_url(url, site, expected):
    """Make sure we correct join a base URL and a possibly relative URL."""
    assert to_absolute_url(url, site) == expected
