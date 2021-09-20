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

import factory
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone
from faker import Factory

from apps.blog.models import Author, Post

faker = Factory.create()


class AuthorFactory(factory.django.DjangoModelFactory):
    first_name = faker.first_name()
    last_name = faker.last_name()
    username = faker.email()
    email = faker.email()
    password = factory.LazyFunction(lambda: make_password('secret'))

    class Meta:
        model = Author


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f'{faker.word()} {n}')
    slug = factory.Sequence(lambda n: f'test-post-{n}')
    body = faker.text()
    author = factory.SubFactory(AuthorFactory)
    created_at = factory.LazyFunction(timezone.now)

    class Meta:
        model = Post

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """
        Override the default _create to allow for the overriding of timestamps.
        See : https://github.com/rbarrois/factory_boy/issues/102
        """
        created_at = kwargs.pop('created_at', None)
        updated_at = kwargs.pop('updated_at', None)
        published_at = kwargs.pop('published_at', None)

        post = super()._create(target_class, *args, **kwargs)
        updated = False

        if created_at is not None:
            updated = True
            post.created_at = created_at

        if updated_at is not None:
            updated = True
            post.updated_at = updated_at

        if published_at is not None:
            updated = True
            post.published_at = published_at

        if updated:
            models.Model.save(post)

        return post
