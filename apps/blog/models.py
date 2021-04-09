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

"""Blog models."""

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from branch.models import AbstractPage


class Author(User):
    """A proxy class to extend default User model."""

    class Meta:
        """Author model metadata class."""

        proxy = True


class Post(AbstractPage):
    """Blog posts model class."""

    featured_image = models.ImageField(
        null=True,
        blank=True,
        upload_to='img/',
        verbose_name=_('Featured image'),
    )

    excerpt = models.TextField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name=_('excerpt'),
        help_text=_('A short, concise introduction'),
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Author'),
    )

    class Meta:
        """Post model metadata class."""

        ordering = ('-published_at',)
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def get_absolute_url(self):
        return reverse('blog:post_view', args=[
            self.published_at.year,  # pylint: disable=no-member
            self.published_at.month,  # pylint: disable=no-member
            self.published_at.day,  # pylint: disable=no-member
            self.slug,
        ])
