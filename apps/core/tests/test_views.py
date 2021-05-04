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
from django.test.utils import override_settings


@pytest.mark.django_db
@override_settings(ALLOW_ROBOTS=True)
def test_sitemap_url(client):
    """Make sure sitemap.xml is present in robots.txt"""
    response = client.get('/robots.txt')
    assert response.status_code == 200

    expected = f'Sitemap: {settings.BASE_URL}/sitemap.xml'
    assert expected in response.content.decode('utf-8')


@pytest.mark.django_db
@override_settings(ALLOW_ROBOTS=False)
def test_disabled_robots(client):
    """Make sure we can disallow everything to be crawled"""
    response = client.get('/robots.txt')
    assert response.status_code == 200
    assert 'User-agent: *\nDisallow: /' in response.content.decode('utf-8')


@pytest.mark.django_db
def test_humans(client):
    response = client.get('/humans.txt')
    assert response.status_code == 200

    content = response.content.decode('utf-8')
    last_update = f'Last update: {settings.BUILD_DATE_SHORT}'

    assert last_update in content
    assert 'CONGRATULATIONS, you found my humans.txt file!' in content
    assert 'Components: Django, jQuery, Ed Theme' in content
