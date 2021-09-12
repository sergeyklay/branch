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

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _
from django_comments.moderation import moderator
from taggit.managers import TaggableManager

from apps.comments.moderation import PostCommentModerator
from apps.core.models import Content


class Author(get_user_model()):
    """A proxy class to extend default User model."""

    class Meta:
        """Author model metadata class."""

        proxy = True


class Post(Content):
    """Blog posts model class."""

    TYPES = (
        ('drama', _('Drama')),
        ('narrative', _('Narrative')),
        ('poem poetry', _('Poem')),
        ('post', _('Post')),
    )

    post_type = models.CharField(
        max_length=12,
        choices=TYPES,
        default='post',
        verbose_name=_('Publication type'),
    )

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
        verbose_name=_('Excerpt'),
        help_text=_('A short, concise introduction.'),
    )

    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('Author'),
    )

    allow_comments = models.BooleanField(
        default=True,
        verbose_name=_('Allow comments'),
        help_text=_('Uncheck to disable comments for this post.'),
    )

    tags = TaggableManager()

    class Meta:
        """Post model metadata class."""

        ordering = ('-published_at',)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def get_absolute_url(self):
        """Tell Django how to generate the canonical URL for a post."""
        return reverse('blog:post_view', args=[
            self.published_at.year,  # pylint: disable=no-member
            self.published_at.month,  # pylint: disable=no-member
            self.published_at.day,  # pylint: disable=no-member
            self.slug,
        ])

    @property
    def is_updated(self):
        """
        Determine if the post has been updated since it was published.

        This function ignores microseconds when comparing post dates.
        """
        # Haha :)
        #
        #   E1123: Unexpected keyword argument 'microsecond' in method call
        #   (unexpected-keyword-arg)
        #
        #   See: https://github.com/PyCQA/pylint-django/issues/194
        #
        # pylint: disable=E1123
        published_at = self.published_at.replace(microsecond=0)
        updated_at = self.updated_at.replace(microsecond=0)

        return updated_at > published_at


class Comment(models.Model):
    """Post comments model class."""

    STATUS_HIDDEN = 'hidden'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = (
        (STATUS_HIDDEN, _('Hidden')),
        (STATUS_PUBLISHED, _('Published')),
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name=_('Post'),
    )

    user_name = models.CharField(
        max_length=40,
        verbose_name=_('User name'),
        help_text=_('The name of the user who posted the comment.'),
    )

    user_email = models.EmailField(
        max_length=254,
        verbose_name=_('E-Mail'),
        help_text=_('The email of the user who posted the comment.'),
    )

    comment = models.TextField(
        verbose_name=_('Comment'),
        help_text=_('The actual content of the comment itself.'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_HIDDEN,
        verbose_name=_('Status'),
        help_text=_('Is the comment will be displayed on the site?')
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

    class Meta:
        """Comment model metadata class."""

        ordering = ('created_at',)
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        """Override the default name of the objects of Comment class."""
        str_id = format_lazy(
            '{msg} {name} {on} "{post}"',
            msg=_('Comment by'),
            name=self.user_name,
            on=_('on'),
            post=self.post,
        )

        return str(str_id)

    def save(self, *args, **kwargs):
        """On save, update updated_at timestamp."""
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)


moderator.register(Post, PostCommentModerator)
