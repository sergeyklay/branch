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

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
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
        unique_for_date='published_at',
        verbose_name=_('Slug'),
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Author'),
    )

    body = models.TextField(
        verbose_name=_('Content'),
    )

    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Published at'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_('Status'),
    )

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # The status-specific manager.

    class Meta:
        ordering = ('-published_at',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_view', args=[
            self.published_at.year,
            self.published_at.month,
            self.published_at.day,
            self.slug,
        ])
