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

    # The change frequency of website pages
    changefreq = 'monthly'

    # The priority tag uses a scale from 0.0 to 1.0.
    # The higher the value, the higher priority the page is.
    priority = 0.5

    def items(self):
        """Get a list of pages."""
        return Page.published.all()

    def lastmod(self, obj):
        """Get the last time the object was modified."""
        return obj.updated_at
