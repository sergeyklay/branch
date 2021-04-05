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

from django.db import models
from django.utils.translation import gettext_lazy as _


class SettingsManager(models.Manager):
    def get(self, name, default=None):
        queryset = super().get_queryset().filter(name=name)
        try:
            return queryset.get(name=name).value
        except self.model.DoesNotExist:
            return default


class Setting(models.Model):
    """Model for site-wide settings."""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name=_('Setting name'),
        help_text=_('Name of site-wide variable'),
    )

    value = models.TextField(
        null=True,
        blank=True,
        max_length=250,
        verbose_name=_('Setting value'),
        help_text=_('Value of site-wide variable that scripts can reference')
    )

    objects = models.Manager()  # The default manager.
    website = SettingsManager()  # The safe manager.

    class Meta:
        ordering = ('name',)
        verbose_name = _('Setting')
        verbose_name_plural = _('Settings')

    def __str__(self):
        return self.name
