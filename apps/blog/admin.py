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

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Class to manage blog posts."""

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
        'published_at',
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
