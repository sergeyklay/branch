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

"""Blog posts template tags."""

from django import template

from apps.blog.models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """Get number of published posts"""
    return Post.published.count()


@register.inclusion_tag('blog/partials/latest-posts.html')
def show_latest_posts(limit=5, offset=0):
    """Return latest blog posts."""
    limit = limit + offset
    latest_posts = Post.published.order_by('-published_at')[offset:limit]
    return {'latest_posts': latest_posts}
