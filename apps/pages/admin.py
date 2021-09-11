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

"""Representation of pages models in the admin interface."""

from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy

from apps.trumbowyg.widgets import AdminTrumbowygWidget, RichTextField
from .models import Page


class PagesForm(forms.ModelForm):
    """Pages post form."""

    body = RichTextField(
        label=gettext_lazy('Content'),
        widget=AdminTrumbowygWidget,
    )

    class Meta:
        """Post form metadata class."""

        model = Page
        fields = '__all__'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Create an admin view of the pages table."""

    form = PagesForm

    list_display = (
        'title',
        'slug_link',
        'updated_at',
        'status',
    )

    list_filter = (
        'status',
        'updated_at',
    )

    prepopulated_fields = {
        'slug': ('title',),
    }

    search_fields = (
        'title',
        'body',
    )

    fieldsets = (
        (gettext_lazy('General content'), {
            'fields': (
                'title',
                'slug',
                'body',
                'status',
                'locale',
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

    @admin.display(ordering='slug', description=gettext_lazy('URL'))
    def slug_link(self, obj):
        """Return a HTML link to website page."""
        url = obj.get_absolute_url()
        return format_html(f'<a href="{url}" target="_blank">{url}</a>')
