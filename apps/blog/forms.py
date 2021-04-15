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

"""Blog related forms."""

from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """Post comment form class."""

    label_class = 'contact-form-label'
    input_class = 'contact-form-input form-input'

    user_name = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={
            'class': input_class,
        })
    )

    user_email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': input_class,
        }),
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 7,
            'class': 'comment-form-textarea form-input',
        }),
    )

    class Meta:
        model = Comment
        fields = ('user_name', 'user_email', 'comment')
