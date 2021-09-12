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
from django.utils.html import format_html
from django.utils.translation import gettext_lazy

from apps.trumbowyg.widgets import AdminTrumbowygWidget, RichTextField
from .models import Comment, Post


class PostForm(forms.ModelForm):
    """Blog post form."""

    excerpt = RichTextField(
        label=gettext_lazy('Excerpt'),
        widget=AdminTrumbowygWidget,
    )

    body = RichTextField(
        label=gettext_lazy('Content'),
        widget=AdminTrumbowygWidget,
    )

    class Meta:
        """Post form metadata class."""

        model = Post
        fields = '__all__'


class BaseAdmin(admin.ModelAdmin):
    """Base ModelAdmin class."""

    unpublished_statuses = ()

    @admin.display(ordering='status', description=gettext_lazy('Status'))
    def object_status(self, obj: Comment):
        """Return custom column for object status."""
        style = 'color:#000;font-weight:600'
        if obj.status in self.unpublished_statuses:
            style = 'color:#8f8f8f'

        return format_html(
            f'<span style="{style}">{obj.get_status_display()}</span>'
        )


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
        (gettext_lazy('General content'), {
            'fields': (
                'title',
                'slug',
                'tags',
                'featured_image',
                'excerpt',
                'body',
                ('author', 'status', 'locale', 'allow_comments',),
                'post_type',
                'published_at',
            ),
        }),
        (gettext_lazy('SEO'), {
            'fields': (
                'meta_title',
                'meta_description',
                'no_index',
            )
        }),
    )
