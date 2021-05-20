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

"""Pages models."""

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from apps.core.models import Content


class Page(Content):
    """Page model class."""

    class Meta:
        """Page model metadata class."""

        ordering = ('title',)
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')

    def get_absolute_url(self):
        """Tell Django how to generate the canonical URL for a page."""
        return reverse('pages:page_view', args=[self.slug])
