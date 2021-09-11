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

"""Filters for core application ModelAdmin classes."""

from abc import ABC

from django.contrib import admin
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType as CTModel
from django.template.defaultfilters import capfirst, dictsort
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy

action_names = {
    ADDITION: 'Addition',
    CHANGE: 'Updating',
    DELETION: 'Deletion',
}


class FilterBase(ABC, admin.SimpleListFilter):
    """Base abstract filter meant for core ModelAdmin filters."""

    def queryset(self, request, queryset):
        """
        Return the filtered queryset.

        Returns the filtered queryset based on the value provided in the
        query string and retrievable via `self.value()`.
        """
        if not self.value():
            return queryset

        dictionary = dict(((self.parameter_name, self.value()),))
        return queryset.filter(**dictionary)


class ActionFilter(FilterBase):
    """Use this filter to only show a specific action."""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('Action')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'action_flag'

    def lookups(self, request, model_admin):
        """
        Return a list of actions tuples.

        The first element in each tuple is the coded value for the option that
        will appear in the URL query. The second element is the human-readable
        name for the action that will appear in the right sidebar.
        """
        return tuple((x[0], gettext_lazy(x[1])) for x in action_names.items())


class UserFilter(FilterBase):
    """Use this filter to only show current users, who appear in the log."""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('User')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'user_id'

    def lookups(self, request, model_admin):
        """
        Return a list of tuples.

        The first element in each tuple is the coded value for the option that
        will appear in the URL query. The second element is the human-readable
        name for the option that will appear in the right sidebar.
        """
        ids = LogEntry.objects.values_list(self.parameter_name).distinct()
        user_model = get_user_model()
        return tuple((u.id, u.get_full_name() or u.username)
                     for u in user_model.objects.filter(pk__in=ids))


class StaffFilter(UserFilter):
    """Use this filter to only show current staff members."""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('Staff')

    def lookups(self, request, model_admin):
        """
        Return a list of tuples.

        The first element in each tuple is the coded value for the option that
        will appear in the URL query. The second element is the human-readable
        name for the option that will appear in the right sidebar.
        """
        user_model = get_user_model()
        return tuple((u.id, u.username)
                     for u in user_model.objects.filter(is_staff=True))


class ContentTypeFilter(admin.SimpleListFilter):
    """Use this filter to only show appropriate content types."""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = gettext_lazy('Content Type')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'content_type'

    def lookups(self, request, model_admin):
        """
        Return a list of tuples.

        The first element in each tuple is the coded value for the option that
        will appear in the URL query. The second element is the human-readable
        name for the option that will appear in the right sidebar.
        """
        qs = CTModel.objects.filter(
            logentry__action_flag__in=action_names.keys()
        ).distinct()

        val_list = []
        for entry in qs:
            model = entry.model_class()
            if not model:
                continue

            val = capfirst(force_text(model._meta.verbose_name_plural))
            val_list.append({
                'name': capfirst(force_text(model._meta.verbose_name_plural)),
                'value': ((entry.pk, val),)
            })

        response = ()
        ordered_list = dictsort(val_list, 'name')
        for o in ordered_list:
            response += o['value']
        return response

    def queryset(self, request, queryset):
        """
        Return the filtered queryset.

        Returns the filtered queryset based on the value provided in the
        query string and retrievable via `self.value()`.
        """
        if not self.value():
            return queryset

        return queryset.filter(content_type_id=self.value())
