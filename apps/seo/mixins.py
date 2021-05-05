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

"""SEO mixins lives here."""


class PageDetailsMixin:
    """Specify page details to the template context."""

    @property
    def title(self):
        """Get resource title."""
        return None

    @property
    def description(self):
        """Get resource description."""
        return None

    @property
    def author(self):
        """Get resource author."""
        return None

    @property
    def locale(self):
        """Get resource locale."""
        return None

    @property
    def resource_type(self):
        """Get resource type."""
        return None

    def get_context_data(self, **kwargs):
        """Get object's context data to use in templates."""
        context = super().get_context_data(**kwargs)  # type: dict
        context.update({
            'seo_title': self.title,
            'seo_description': self.description,
            'seo_author': self.author,
            'seo_locale': self.locale,
            'seo_type': self.resource_type,
        })

        return context
