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
from django.urls import reverse

from .factories import PostFactory


@pytest.mark.django_db
def test_post_standard_meta_tags(author, client):
    """Make sure we generate standard meta tags."""
    post = PostFactory(
        author=author,
        title='Hello, World!',
        excerpt='Lorem ipsum',
        status='published',
    )

    url = post.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200

    content = response.content.decode('utf-8')

    assert 'Hello, World!' in content
    assert '<title>Hello, World! - ' in content
    assert '<meta property="dc:title" content="Hello, World!">' in content
    assert '<meta property="og:title" content="Hello, World!">' in content

    assert '<meta name="description" content="Lorem ipsum">' in content
    assert '<meta property="dc:description" content="Lorem ipsum">' in content
    assert '<meta property="og:description" content="Lorem ipsum">' in content


@pytest.mark.django_db
def test_post_seo_meta_tags(author, client):
    """Make sure we generate SEO meta tags."""
    post = PostFactory(
        author=author,
        title='Hello, World II!',
        meta_title='Alternative title',
        excerpt='Lorem ipsum',
        meta_description='description',
        status='published',
    )

    url = post.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200

    content = response.content.decode('utf-8')

    assert 'Hello, World II!' in content
    assert '<title>Alternative title - ' in content
    assert '<meta property="dc:title" content="Alternative title">' in content
    assert '<meta property="og:title" content="Alternative title">' in content

    assert '<meta name="description" content="description">' in content
    assert '<meta property="dc:description" content="description">' in content
    assert '<meta property="og:description" content="description">' in content


@pytest.mark.django_db
def test_post_tags_notfound(client):
    """Request to a non-existent tag should lead to 404 error."""
    response = client.get(reverse('blog:post_list_by_tag', args=('foo',)))
    assert response.status_code == 404


@pytest.mark.django_db
def test_post_tags_notfound2(client):
    """Request to a existent tag should return all tagged posts."""
    post = PostFactory()
    post.tags.add('red', 'green')

    response = client.get(reverse('blog:post_list_by_tag', args=('red',)))
    assert response.status_code == 200

    response = client.get(reverse('blog:post_list_by_tag', args=('green',)))
    assert response.status_code == 200
