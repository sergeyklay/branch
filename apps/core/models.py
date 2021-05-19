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

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PublishedManager(models.Manager):
    """Custom models manager get only published posts and pages."""

    def get_queryset(self):
        """Return a QuerySet object with predefined filters."""
        return super().get_queryset().filter(status='published')


class Content(models.Model):
    """
    Basic page data which can be used by other modules.

    This class is intended to abstract some common features:

    * Adds common page fields like title, slug, body, etc.
    * Adds automatic timestamps fields to the model.
    * Adds locale field.
    * Adds SEO-related fields.
    """

    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
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
        help_text=_('Leave it blank for automatic populating.'),
    )

    no_index = models.BooleanField(
        default=False,
        verbose_name=_('Block search indexing'),
        help_text=_('Prevent this page from appearing in search index.'),
    )

    body = models.TextField(
        verbose_name=_('Full text of the post'),
    )

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

    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('First publication date'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status'),
    )

    locale = models.CharField(
        max_length=5,
        choices=settings.LOCALE_TERRITORY,
        default='en_US',
        verbose_name=_('Locale'),
        help_text=_('Specify the publishing locale used.'),
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
        """Basic page metadata class."""

        abstract = True

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        """Tell Django how to generate the canonical URL for a post or page."""
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        """On save, update updated_at timestamp."""
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
