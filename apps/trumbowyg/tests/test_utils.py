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

from apps.trumbowyg.utils import content_sanitize


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
    assert content_sanitize(raw_text) == expected


@pytest.mark.parametrize(
    'raw_text,allowed_tags,expected',
    [
        ('<a>word</a>', ('a',), '<a>\n word\n</a>'),
        ('<a data="xxx">word</a>', ('a',), '<a>\n word\n</a>'),
        ('<a style="xxx">word</a>', ('a',), '<a style="xxx">\n word\n</a>'),
    ]
)
def test_content_sanitize_allowed_tags(raw_text, allowed_tags, expected):
    assert content_sanitize(raw_text, allowed_tags) == expected
