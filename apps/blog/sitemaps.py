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

"""Blog sitemap module."""

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Post
from .urls import app_name


class PostSitemap(Sitemap):
    """Blog sitemap configuration."""

    # The change frequency of blog post pages
    changefreq = 'monthly'

    # The priority tag uses a scale from 0.0 to 1.0.
    # The higher the value, the higher priority the page is.
    priority = 0.8

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        """Get the last time the object was modified."""
        return obj.updated_at


class PostsListSitemap(Sitemap):
    """Provide configuration for blog dynamic pages."""

    # The change frequency of telegraph pages
    changefreq = 'daily'

    # The priority tag uses a scale from 0.0 to 1.0.
    # The higher the value, the higher priority the page is.
    priority = 0.9

    def items(self):
        return ['post_list']

    def location(self, item):
        return reverse(f'{app_name}:{item}')
