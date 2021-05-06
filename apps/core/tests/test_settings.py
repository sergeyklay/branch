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

import os

import environ
import pytest
from django.conf import settings

from branch.settings.base import get_db_config


@pytest.mark.parametrize(
    'key', ('APPS_DIR', 'STATIC_ROOT', 'MEDIA_ROOT')
)
def test_base_paths_presents(key):
    """Make sure all relevant base paths exists."""
    assert isinstance(getattr(settings, key), str)
    assert len(getattr(settings, key)) > 0


@pytest.mark.parametrize(
    'key', ('SITE_NAME', 'SITE_DESCRIPTION', 'SITE_TAGLINE',
            'CONTACT_EMAIL', 'SERVER_EMAIL',
            'COPYRIGHT_HOLDER',
            'GITHUB_USER', 'PAGE_SIZE')
)
def test_important_vars_presents(key):
    """Make sure all important variables are present."""
    assert getattr(settings, key, None) is not None


def test_get_db_config(monkeypatch):
    """Make sure we resolve relative db path."""
    env = environ.Env()

    def mock_database_url(env_vars):
        env_vars['DATABASE_URL'] = 'sqlite:///db.sqlite3'
        return env_vars

    monkeypatch.setattr(env, 'ENVIRON', mock_database_url(env.ENVIRON))

    option = env.str('DATABASE_URL')

    assert isinstance(option, str)
    assert not os.path.isabs(option)

    options = get_db_config('DATABASE_URL')
    assert 'NAME' in options
    assert os.path.isabs(options['NAME'])
