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

"""Representation of blog models in the admin interface."""

from django import forms
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.trumbowyg.widgets import AdminTrumbowygWidget, RichTextField
from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Blog post form."""

    excerpt = RichTextField(
        label=_('Excerpt'),
        widget=AdminTrumbowygWidget,
    )

    body = RichTextField(
        label=_('Content'),
        widget=AdminTrumbowygWidget,
    )

    class Meta:
        """Post form metadata class."""

        model = Post
        fields = '__all__'


class BaseAdmin(admin.ModelAdmin):
    """Base ModelAdmin class."""

    unpublished_statuses = ()

    def object_status(self, obj: Comment):
        """Return custom column for object status."""
        style = 'color:#000;font-weight:600'
        if obj.status in self.unpublished_statuses:
            style = 'color:#8f8f8f'

        return mark_safe(
            '<span style="{}">{}</span>'.format(
                style,
                obj.get_status_display()
            )
        )
    object_status.allow_tags = True
    object_status.short_description = _('Status')
    object_status.admin_order_field = 'status'


@admin.register(Post)
class PostAdmin(BaseAdmin):
    """Class to manage blog posts."""

    form = PostForm

    list_display = (
        'title',
        'slug',
        'object_status',
        'published_at',
    )

    list_display_links = (
        'title',
    )

    list_filter = (
        'status',
        'created_at',
        'published_at',
    )

    search_fields = (
        'title',
        'excerpt',
        'body',
    )

    prepopulated_fields = {
        'slug': ('title',),
    }

    date_hierarchy = 'published_at'

    ordering = (
        'status',
        '-published_at',
    )

    unpublished_statuses = (
        'draft',
    )

    fieldsets = (
        (_('General content'), {
            'fields': (
                'title',
                'slug',
                'featured_image',
                'excerpt',
                'body',
                'author',
                'status',
                'locale',
                'post_type',
                'published_at',
            ),
        }),
        (_('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
                'no_index',
            )
        }),
    )


@admin.register(Comment)
class CommentAdmin(BaseAdmin):
    """Class to manage post comments."""

    list_display = (
        'comment_sender',
        'comment_content',
        'post',
        'object_status',
        'created_at',
    )

    list_display_links = (
        'comment_content',
    )

    list_filter = (
        'status',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user_name',
        'user_email',
        'comment',
    )

    fieldsets = (
        (_('Commentator'), {
            'fields': (
                'user_name',
                'user_email',
            ),
        }),
        (_('Comment'), {
            'fields': (
                'comment',
                'status',
            )
        }),
    )

    unpublished_statuses = (
        Comment.STATUS_HIDDEN,
    )

    actions = (
        'publish_comments',
        'unpublish_comments',
    )

    @admin.action(description=_('Publish selected comments'))
    def publish_comments(self, request, queryset: QuerySet):
        """Publish selected comments."""
        rows = queryset.update(
            status=Comment.STATUS_PUBLISHED
        )
        if rows > 0:
            message = _('Selected comments published successfully')
            self.message_user(request, message, messages.SUCCESS)
        else:
            self.message_user(request, _('Nothing has been changed'))

    @admin.action(description=_('Unpublish selected comments'))
    def unpublish_comments(self, request, queryset: QuerySet):
        """Unpublish selected comments."""
        rows = queryset.update(
            status=Comment.STATUS_HIDDEN
        )
        if rows > 0:
            message = _('Selected comments unpublished successfully')
            self.message_user(request, message, messages.SUCCESS)
        else:
            self.message_user(request, _('Nothing has been changed'))

    def comment_sender(self, obj):
        """Return custom column for comment sender."""
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:blog_comment_change", args=(obj.pk,)),
            (obj.user_name or obj.user_email)
        ))
    comment_sender.allow_tags = True
    comment_sender.short_description = _('Sender')
    comment_sender.admin_order_field = 'user_name'

    def comment_content(self, obj):
        """Return custom column for comment comment."""
        data = obj.comment.replace('\n', '')
        return (data[:120] + '..') if len(data) > 120 else data
    comment_content.short_description = _('Comment')
    comment_content.admin_order_field = 'content'
