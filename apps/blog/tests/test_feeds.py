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
from django.urls import reverse
from django.utils import timezone
from pyquery import PyQuery

from .factories import PostFactory


@pytest.mark.django_db
def test_posts_rss_no_items(client):
    response = client.get(reverse('blog:posts_rss'))

    assert response.status_code == 200
    assert response.headers['content-type'] == (
        'application/rss+xml; charset=utf-8'
    )

    pq = PyQuery(response.content, parser='xml')

    assert pq('title').text().startswith('Latest posts - ')
    assert pq('link').text() == f'{settings.BASE_URL}/feeds/rss/posts.xml'
    assert pq('description').text() == settings.SITE_DESCRIPTION
    assert pq('language').text() == 'en-us'
    assert pq('copyright').text().startswith('Copyright (c) 2018-')


@pytest.mark.django_db
@pytest.mark.parametrize('execution_number', range(5))
def test_posts_rss_items(author, client, execution_number):
    date = timezone.now()
    PostFactory(
        author=author,
        title=f'Hello, World #{execution_number}!',
        excerpt='Lorem ipsum',
        status='published',
        slug=f'test-post-{execution_number}',
        published_at=date,
    )

    PostFactory(author=author, title=f'Some draft #{execution_number}')

    response = client.get(reverse('blog:posts_rss'))
    pq = PyQuery(response.content)

    assert response.headers['content-type'] == (
        'application/rss+xml; charset=utf-8'
    )

    assert response.status_code == 200
    assert len(pq('channel item')) == 1
    assert pq('channel item description').text() == 'Lorem ipsum'

    assert pq('channel item title').text() == (
        f'Hello, World #{execution_number}!'
    )

    assert pq('channel item link').text() == (
        f'{settings.BASE_URL}/post/'
        f'{date.strftime("%Y/%m/%d").replace("/0", "/")}'
        f'/test-post-{execution_number}.html'
    )
