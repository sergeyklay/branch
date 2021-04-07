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
from django.conf import settings
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .forms import RichTextField
from .models import Post


class PostForm(forms.ModelForm):
    """Blog post form."""

    body = RichTextField(label=_('Content'))

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

    raw_id_fields = (
        'author',
    )

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

    class Media:
        """
        PostAdmin metadata class.

        Setup static assets to use in WYSIWYG editor.
        """

        css = {
            'all': (
                'trumbowyg/dist/ui/trumbowyg{}.css'.format(
                    '' if settings.DEBUG else '.min',
                ),
            ),
        }

        js = (
            'admin/js/jquery.init.js',
            'js/shared.js',
            'trumbowyg/dist/trumbowyg{}.js'.format(
                '' if settings.DEBUG else '.min',
            ),
            'trumbowyg/dist/plugins/upload/trumbowyg.upload{}.js'.format(
                '' if settings.DEBUG else '.min',
            ),
            'admin/js/richtext.editor.js'
        )
