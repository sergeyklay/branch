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

"""Project wide models lives here."""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PublishedManager(models.Manager):
    """Custom models manager get only published posts and pages."""

    def get_queryset(self):
        """Return a QuerySet object with predefined filters."""
        return super().get_queryset().filter(status='published')


class AbstractPage(models.Model):
    """Abstract base model class for all kinds of posts and pages."""

    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
    )

    LOCALES = (
        ('en_US', _('English')),
        ('ru_RU', _('Russian')),
        ('uk_UA', _('Ukrainian')),
    )

    title = models.CharField(
        max_length=250,
        verbose_name=_('Title'),
    )

    slug = models.SlugField(
        max_length=250,
        db_index=True,
        unique_for_date='published_at',
        verbose_name=_('Slug'),
        help_text=_('Let it empty so it will be autopopulated.'),
    )

    no_index = models.BooleanField(
        default=False,
        verbose_name=_('Block search indexing'),
        help_text=_('Prevent this page from appearing in search index'),
    )

    body = models.TextField(
        verbose_name=_('Full text of the post'),
    )

    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('First publication date'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date created'),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Date updated'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status'),
    )

    locale = models.CharField(
        max_length=5,
        choices=LOCALES,
        default='en_US',
        verbose_name=_('Locale'),
        help_text=_('The locale of the resource.'),
    )

    meta_title = models.CharField(
        max_length=60,
        blank=True,
        default='',
        verbose_name=_('Meta title'),
        help_text=_('This will be displayed in meta tags. '
                    'Keep it under 60 characters. '
                    "Leave empty and the post's title will be used."),
    )

    meta_description = models.TextField(
        max_length=256,
        blank=True,
        default='',
        verbose_name=_('Meta description'),
        help_text=_('This will be displayed in meta tags. '
                    'Keep it under 120 characters.')
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The status-specific manager.

    class Meta:
        """Abstract base model metadata class."""

        abstract = True

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """Tell Django how to generate the canonical URL for a post or page."""
        raise NotImplementedError()
