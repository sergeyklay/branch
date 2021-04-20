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

from apps.trumbowyg import utils


@pytest.mark.parametrize(
    'raw_text,expected',
    [
        ('', ''),
        ('simple text\n', 'simple text'),
        ('simple text', 'simple text'),
        ('[simple text]', '[simple text]'),
        ('<a>word</a>', 'word'),
        ('<p>word</p>', '<p>\n word\n</p>'),
        ('<script></script>', ''),
        ('<style></style>', ''),
    ]
)
def test_content_sanitize_simple_usage(raw_text, expected):
    assert utils.content_sanitize(raw_text) == expected


@pytest.mark.parametrize(
    'raw_text,allowed_tags,expected',
    [
        ('<a>word</a>', ('a',), '<a>\n word\n</a>'),
        ('<a data="xxx">word</a>', ('a',), '<a>\n word\n</a>'),
        ('<a style="xxx">word</a>', ('a',), '<a style="xxx">\n word\n</a>'),
    ]
)
def test_content_sanitize_allowed_tags(raw_text, allowed_tags, expected):
    assert utils.content_sanitize(raw_text, allowed_tags) == expected


@pytest.mark.parametrize(
    'raw_text,expected',
    [
        ('“hello“', '"hello"'),
        ('”hello”', '"hello"'),
        ('’hello’', "'hello'"),
        ('‘hello‘', "'hello'"),
        ('“‘”‘', '"\'"\''),
    ]
)
def test_content_sanitize_quotes(raw_text, expected):
    assert utils.content_sanitize(raw_text) == expected


@pytest.mark.parametrize(
    'raw_text,unescape_tags,expected',
    [
        ('&lt;h1&gt;', True, ''),
        ('&lt;h1&gt;Hello&lt;/h1&gt;', True, '<h1>\n Hello\n</h1>'),
        ('&lt;h1&gt;Hello&lt;/h1&gt;', False, '&lt;h1&gt;Hello&lt;/h1&gt;'),
    ]
)
def test_content_sanitize_unescape_tags(raw_text, unescape_tags, expected):
    assert utils.content_sanitize(raw_text, unescape_tags=unescape_tags) == expected


@pytest.mark.parametrize(
    'lang,expected',
    [
        ('', None),
        (None, None),
        (True, None),
        ('ru_RU', 'ru'),
        ('en', None),
        ('no_nb', 'no_nb'),
        ('vi', 'vi'),
        ('zh_tw', 'zh_tw'),
        ('fu', None),
    ]
)
def test_accepted_language(lang, expected):
    assert utils.get_trumbowyg_language(lang) == expected
