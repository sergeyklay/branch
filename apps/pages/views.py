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

"""Pages views definitions."""

from django.views.generic import DetailView

from branch.mixins import PageDetailsMixin
from .models import Page


class PageDetailView(PageDetailsMixin, DetailView):
    """Display a page detail."""

    model = Page
    context_object_name = 'page'
    template_name = 'pages/pages/view.html'
    queryset = Page.published.all()

    @property
    def title(self):
        if self.object.meta_title:
            return self.object.meta_title

        if self.object.title:
            return self.object.title

        return None

    @property
    def description(self):
        if self.object.meta_description:
            return self.object.meta_description

        return None

    @property
    def locale(self):
        return self.object.locale
