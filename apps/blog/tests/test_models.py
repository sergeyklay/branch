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

import datetime

import pytest

from .factories import PostFactory


@pytest.mark.django_db
def test_post_is_updated(author):
    post = PostFactory(author=author)

    assert post.is_updated is False
    assert post.published_at.replace(microsecond=0) == \
           post.updated_at.replace(microsecond=0)

    post = PostFactory(
        author=author,
        updated_at=post.updated_at + datetime.timedelta(minutes=31)
    )

    assert post.is_updated is True
    assert post.published_at.replace(microsecond=0) != \
           post.updated_at.replace(microsecond=0)
