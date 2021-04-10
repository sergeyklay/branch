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
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from branch.forms import RichTextField
from branch.utils import RichTextAdminMedia
from .models import Page


class PagesForm(forms.ModelForm):
    """Pages post form."""

    body = RichTextField(label=_('Content'))

    class Meta:
        """Post form metadata class."""

        model = Page
        fields = '__all__'


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """Class to manage pages."""

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
        (_('General content'), {
            'fields': (
                'title',
                'slug',
                'body',
                'status',
                'locale',
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

    def slug_link(self, obj):
        """Resolve link to website page."""
        url = obj.get_absolute_url()
        return mark_safe(f'<a href="{url}" target="_blank">{url}</a>')
    slug_link.allow_tags = True
    slug_link.short_description = _('URL')
    slug_link.admin_order_field = 'slug'

    class Media(RichTextAdminMedia):
        """PageAdmin metadata class."""
