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

"""Telegraph sitemap module."""

from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .urls import app_name


class TelegraphSitemap(Sitemap):
    """Telegraph sitemap configuration."""

    # The change frequency of telegraph pages
    changefreq = 'yearly'

    # The priority tag uses a scale from 0.0 to 1.0.
    # The higher the value, the higher priority the page is.
    priority = 0.4

    def items(self):
        return ['contact_form']

    def location(self, item):
        return reverse(f'{app_name}:{item}')
