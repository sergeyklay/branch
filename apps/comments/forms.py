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

"""Comments forms module."""

from django import forms
from django.utils.translation import gettext_lazy, pgettext_lazy
from django_comments.forms import COMMENT_MAX_LENGTH, CommentForm


class PostCommentForm(CommentForm):
    """
    Handles the specific details of the comment (name, comment, etc.).

    The main comment form representing the standard way of handling submitted
    comments.
    """

    label_class = 'comment-form-label'
    input_class = 'comment-form-input form-input'

    name = forms.CharField(
        label=pgettext_lazy('Person name', 'Name'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': input_class,
        })
    )

    email = forms.EmailField(
        label=gettext_lazy('Email address'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': input_class,
        }),
    )

    honeypot = forms.CharField(
        required=False,
        label=gettext_lazy(
            'If you enter anything in this field '
            'your comment will be treated as spam'
        ),
    )

    url = forms.URLField(
        label=gettext_lazy('URL'),
        max_length=254,
        required=False,
        widget=forms.URLInput(attrs={
            'class': input_class,
        }),
    )

    comment = forms.CharField(
        label=gettext_lazy('Comment'),
        max_length=COMMENT_MAX_LENGTH,
        widget=forms.Textarea(attrs={
            'rows': 7,
            'class': 'comment-form-textarea form-input',
        }),
    )
