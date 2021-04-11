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

"""Website models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class SettingsManager(models.Manager):
    """Custom models manager to safe get website settings."""

    def get(self, name, default=None):
        """Safe getter for website settings."""
        queryset = super().get_queryset().filter(name=name)
        try:
            return queryset.get(name=name).value
        except self.model.DoesNotExist:
            return default


class Setting(models.Model):
    """Model for site-wide settings."""

    name = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name=_('Setting name'),
    )

    value = models.TextField(
        null=True,
        blank=True,
        max_length=150,
        verbose_name=_('Setting value'),
    )

    objects = models.Manager()  # The default manager.
    website = SettingsManager()  # The safe manager.

    class Meta:
        """Setting model metadata class."""

        ordering = ('name',)
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return f'{self.name}'
