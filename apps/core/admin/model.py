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

"""ModelAdmin classes for core application administration."""

from django.contrib import admin
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import LogEntry
from django.template.defaultfilters import capfirst, truncatewords
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape
from django.utils.html import format_html
from django.utils.translation import gettext_lazy

from .filters import (
    action_names,
    ActionFilter,
    ContentTypeFilter,
    StaffFilter,
    UserFilter,
)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Create an admin view of the history/log table."""

    date_hierarchy = 'action_time'

    list_filter = (
        UserFilter,
        StaffFilter,
        ActionFilter,
        ContentTypeFilter,
    )

    search_fields = (
        'object_repr',
        'change_message',
    )

    list_display = (
        'action_time',
        'user',
        'action_description',
        'get_contenttype',
        'object_link',
        'get_change_message',
    )

    fieldsets = (
        (gettext_lazy('Metadata'), {
            'fields': (
                'action_time',
                'user',
                'action_description',
                'object_link',
            ),
        }),
        (gettext_lazy('Details'), {
            'fields': (
                'get_change_message',
                'get_contenttype',
                'object_id',
                'object_repr',
            )
        })
    )

    def has_add_permission(self, request):
        """Disallow creating new log entries."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disallow editing log entries."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disallow deleting log entries."""
        return False

    def has_module_permission(self, request):
        """Set the given request as having perms in the given app label."""
        return True

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances.

        This is used by changelist_view.
        """
        qs = super().get_queryset(request).prefetch_related('content_type')
        if not request.user.is_superuser:
            return qs.filter(user__id=request.user.pk)
        return qs

    @admin.display(
        ordering='object_repr',
        description=gettext_lazy('Object repr'),
    )
    def object_link(self, obj):
        """Return custom column for object link."""
        obj_repr = escape(obj.object_repr)
        ct = obj.content_type
        try:
            url = f'admin:{ct.app_label}_{ct.model}_change'
            link = '<a href="{}">{}</a>'.format(
                reverse(url, args=[obj.object_id]),
                obj_repr
            )
        except NoReverseMatch:
            link = obj_repr
        return format_html(link) if obj.action_flag != DELETION else obj_repr

    @admin.display(ordering='action_flag', description=gettext_lazy('Action'))
    def action_description(self, obj):
        """Return custom column for action description."""
        verbose = action_names[obj.action_flag]
        return gettext_lazy(verbose)

    @admin.display(
        ordering='content_type__model',
        description=gettext_lazy('Content Type'),
    )
    def get_contenttype(self, obj):
        """Return custom column for content type."""
        return capfirst(obj.content_type)

    @admin.display(description=gettext_lazy('Comment'))
    def get_change_message(self, obj):
        """Return custom column for change message."""
        return truncatewords(obj.get_change_message(), 10)
