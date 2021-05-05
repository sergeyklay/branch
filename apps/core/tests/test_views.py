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

from apps.core import views
from branch import urls


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
    """Make sure humans.txt is rendered properly"""
    response = client.get('/humans.txt')
    assert response.status_code == 200

    content = response.content.decode('utf-8')
    last_update = f'Last update: {settings.BUILD_DATE_SHORT}'

    assert last_update in content
    assert 'CONGRATULATIONS, you found my humans.txt file!' in content
    assert 'Components: Django, jQuery, Ed Theme' in content


@pytest.mark.django_db
def test_404_app(client):
    """Make sure 404 handler worked as expected."""
    response = client.get('/xxxxxxx')
    assert urls.handler404 == 'apps.core.views.handler404'
    assert response.status_code == 404
    assert 'core/404.html' in (t.name for t in response.templates)

    content = response.content.decode('utf-8')
    assert 'Page Not Found.' in content
    assert 'Latest publications' in content


@pytest.mark.django_db
@pytest.mark.ignore_template_errors
def test_500_app(rf):
    """Simulate 500 error."""
    request = rf.get('/')
    response = views.handler500(request)
    assert urls.handler500 == 'apps.core.views.handler500'
    assert response.status_code == 500

    content = response.content.decode('utf-8')
    assert 'Oops! Website has an error.' in content
    assert 'Latest publications' in content


@pytest.mark.django_db
@pytest.mark.ignore_template_errors
@pytest.mark.urls('apps.core.tests.urls')
@override_settings(MIDDLEWARE=())
def test_500_before_middlewares(client):
    """Simulate an early 500 causing middlewares breakage."""
    response = client.get('/500')
    assert response.status_code == 500
    assert 'core/500.html' in (t.name for t in response.templates)

    content = response.content.decode('utf-8')
    assert 'Oops! Website has an error.' in content
    assert 'Latest publications' in content
