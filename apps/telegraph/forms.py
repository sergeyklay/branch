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

"""Telegraph related forms."""

from django import forms
from django.utils.translation import gettext_lazy as _


class ContactMessageForm(forms.Form):
    """Contact message form class."""

    label_class = 'contact-form-label'
    input_class = 'contact-form-input form-input'

    name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': input_class,
            'placeholder': _('How can I contact you'),
        })
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': input_class,
            'placeholder': _('Where can I send a response'),
        }),
    )

    subject = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(attrs={
            'class': input_class,
            'placeholder': _('Can be blank'),
        }),
    )

    gotcha = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'class': 'contact-form-gotcha',
        })
    )

    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={
            'rows': 7,
            'class': 'contact-form-textarea form-input'
        }),
    )
