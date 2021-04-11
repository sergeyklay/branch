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

"""Pages sitemap module."""

from django.contrib.sitemaps import Sitemap

from .models import Page


class PageSitemap(Sitemap):
    """Pages sitemap configuration."""

    # The change frequency of blog post pages
    changefreq = 'monthly'

    # The blog post relevance in website
    priority = 0.6

    def items(self):
        return Page.published.all()

    def lastmod(self, obj):
        """Get the last time the object was modified."""
        return obj.updated_at
