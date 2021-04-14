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

"""Representation of website models in the admin interface."""

from django import forms
from django.contrib import admin
from django.db import models

from .models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    """Class to manage website settings."""

    formfield_overrides = {
        models.TextField: {
            'widget': forms.TextInput(
                attrs={
                    'class': 'vTextField',
                    'style': 'min-width: 80%;',
                }
            )
        }
    }

    list_display = (
        'name',
        'value',
    )

    search_fields = (
        'name',
        'value',
    )
