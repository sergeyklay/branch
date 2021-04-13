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

from branch.templatetags.urlparams import urlparams
import pytest


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
