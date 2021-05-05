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

"""Global pylint configuration for all apps."""

import pytest
from django.core.management import call_command

fixtures = ['settings', 'sites']


# pylint: disable=W0621
@pytest.fixture(autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Populate Django test database with pytest fixtures."""
    with django_db_blocker.unblock():
        call_command('loaddata', *[f'{fixture}.json' for fixture in fixtures])
