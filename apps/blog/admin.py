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
from django.contrib import admin
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Class to manage blog posts."""

    form = PostForm

    list_display = (
        'title',
        'slug',
        'author',
        'published_at',
        'status',
    )

    list_filter = (
        'status',
        'created_at',
        'published_at',
        'author',
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
class CommentAdmin(admin.ModelAdmin):
    """Class to manage post comments."""

    class Media:
        """Provide custom assets for CommentAdmin class."""

        css = {
            'all': (
                'admin/css/comment.css',
            )
        }

    list_display = (
        'comment_status',
        'comment_sender',
        'post',
        'content',
        'sent_date',
    )

    list_display_links = (
        'comment_sender',
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

    def comment_status(self, obj):
        """Return custom column for comment status."""
        return mark_safe(
            '<span class="comment-icon comment-icon-{}"></span>'.format(
                obj.status
            )
        )
    comment_status.allow_tags = True
    comment_status.short_description = _('Status')
    comment_status.admin_order_field = 'status'

    def comment_sender(self, obj):
        """Return custom column for comment sender."""
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:blog_comment_change", args=(obj.pk,)),
            (obj.user_name or obj.user_email)
        ))
    comment_sender.allow_tags = True
    comment_sender.short_description = _('Sender')
    comment_sender.admin_order_field = 'user_name'

    def content(self, obj):
        """Return custom column for comment comment."""
        return obj.comment.replace('\n', '')
    content.short_description = _('Comment')
    content.admin_order_field = 'content'

    def sent_date(self, obj):
        """Return custom column for comment sent date."""
        return obj.created_at.strftime("%b %d")
    sent_date.short_description = _('Sent')
    sent_date.admin_order_field = 'created_at'
