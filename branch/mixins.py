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

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ModelTimestampsMixin(models.Model):
    """
    Timestamps aware model mixin.

    Specify created_at and updated_at fields for a model.
    """

    # Do not use 'auto_now_add=True' here to be
    # able override created_at field easily in tests.
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date created'),
    )

    # Do not use 'auto_now=True' here to be
    # able override updated_at field easily in tests.
    updated_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date updated'),
    )

    class Meta:
        """Mixin metadata class."""

        abstract = True

    def save(self, *args, **kwargs):
        """On save, update updated_at timestamp"""
        self.updated_at = timezone.now
        return super().save(*args, **kwargs)


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
    def type(self):
        """Get resource type."""
        return None

    def get_context_data(self, **kwargs):
        """Get object's context data to use in templates."""
        context = super().get_context_data(**kwargs)

        if self.title:
            context['page_title'] = self.title

        if self.description:
            context['page_description'] = self.description

        if self.author:
            context['page_author'] = self.author

        if self.locale:
            context['page_locale'] = self.locale

        if self.type:
            context['page_type'] = self.type

        return context
