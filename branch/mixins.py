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

"""Project wide mixins lives here."""


class PageDetailsMixin:
    """Pass a defined title to context"""

    description = None
    title = None
    author = None

    def get_title(self):
        """Get object title."""
        return self.title

    def get_description(self):
        """Get description title."""
        return self.description

    def get_author(self):
        """Get object author."""
        return self.author

    def get_context_data(self, **kwargs):
        """Get object's context data to use in templates."""
        context = super().get_context_data(**kwargs)

        title = self.get_title()
        if title:
            context['page_title'] = title

        description = self.get_description()
        if description:
            context['page_description'] = description

        author = self.get_author()
        if author:
            context['page_author'] = author

        return context
