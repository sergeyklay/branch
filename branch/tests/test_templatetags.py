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

from datetime import datetime, timezone, timedelta

import pytest

from branch.templatetags.date_to_xmlschema import date_to_xmlschema
from branch.templatetags.urlparams import urlparams


@pytest.mark.parametrize(
    'provided,expected',
    [
        ([[], {}], ''),
        ([['a', 'b', 'c'], {}], ''),
        ([[], {'page': '1'}], '?page=1'),
        ([['a', 'b', 'c'], {'page': '1'}], '?page=1'),
        ([[], {'page': None, 'q': 42}], '?q=42'),
        ([[], {'q': 'search query'}], '?q=search%20query'),
        ([[], {'page': '1', 'q': 'test'}], '?page=1&q=test'),
    ]
)
def test_urlparams(provided, expected):
    args = provided[0]
    kwargs = provided[1]

    assert urlparams(*args, **kwargs) == expected


@pytest.mark.parametrize(
    'provided,expected',
    [
        ('', ''),
        (None, ''),
        ([], ''),
        ('Hello', ''),
        (42, ''),
        (datetime(1983, 1, 1), '1983-01-01T00:00:00'),
        (datetime(1985, 4, 12, 0, 0, 0, 0, timezone(timedelta(hours=3))),
         '1985-04-12T00:00:00+03:00'),
        (datetime(2021, 1, 1, 0, 0, 0, 999, timezone(timedelta(hours=2))),
         '2021-01-01T00:00:00+02:00'),
    ]
)
def test_date_to_xmlschema(provided, expected):
    assert date_to_xmlschema(provided) == expected
