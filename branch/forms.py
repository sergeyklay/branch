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

"""Project wide forms lives here."""

from django import forms

from branch.utils import content_sanitize


class RichTextField(forms.CharField):
    """
    A text field with a rich text editor.

    This class does two main things:
    - add a css class to trigger the rich js text editor
    - sanitize the generated html
    """

    CSS_CLASS = 'textarea-wysiwyg'

    def __init__(self, *args, widget=None, **kwargs):
        widget = widget or forms.Textarea
        super().__init__(*args, widget=widget, **kwargs)

    def widget_attrs(self, widget):
        """Add a custom css class to the widget."""

        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': self.CSS_CLASS
        })

        return attrs

    def clean(self, value):
        """
        Validate the given contents and return its sanitized value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        cleaned = super().clean(value)
        extra_attrs = ('style', 'title', 'class', 'id',)
        extra_tags = (
            'a',
            'abbr',
            'blockquote',
            'code',
            'pre',
            'span',
            'header',
            'footer',
            'img',
            'superscript',
            'subscript',
        )

        contents = content_sanitize(
            cleaned,
            allowed_tags=extra_tags,
            allowed_attrs=extra_attrs,
        )

        return contents.strip()
