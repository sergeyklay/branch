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

from apps.core.utils import to_language


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
    """Make sure we correct transform locale to language"""
    assert to_language(locale) == expected