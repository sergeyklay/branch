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

"""Trumbowyg widgets."""

from django import forms
from django.conf import settings as django_settings
from django.contrib.admin import widgets
from django.utils.translation import get_language

from .utils import get_trumbowyg_language, highlight_js


class TrumbowygWidget(forms.Textarea):
    """
    Widget class to add a Trumbowyg instance on a textarea.

    Take the same arguments than ``forms.Textarea``.
    """

    template_name = 'trumbowyg/forms/widgets/textarea.html'

    @property
    def assets(self):
        """Get static assets to use in WYSIWYG editor."""
        min_js = '' if getattr(django_settings, 'DEBUG', False) else '.min'

        css = (
            'prismjs/themes/prism.css',
            f'trumbowyg/dist/ui/trumbowyg{min_js}.css',
            f'trumbowyg/dist/plugins/highlight/ui/trumbowyg.highlight{min_js}.css',  # noqa
        )

        js = (
            'trumbowyg/js/trumbowyg.config.js',
            f'trumbowyg/dist/trumbowyg{min_js}.js',
        )

        return css, js

    @property
    def media(self):
        """Add necessary files (Js/CSS) to the widget's medias."""
        css, js = self.assets
        return forms.Media(css={'all': css}, js=js)


class AdminTrumbowygWidget(TrumbowygWidget, widgets.AdminTextareaWidget):
    """
    Trumbowyg widget class suited for usage in models admins.

    Acts like ``TrumbowygWidget`` but enables additional plugins.
    """

    @property
    def assets(self):
        """Get static assets to use in WYSIWYG editor."""
        min_js = '' if getattr(django_settings, 'DEBUG', False) else '.min'
        css, _ = super().assets

        js = [
            'admin/js/jquery.init.js',
            'trumbowyg/js/trumbowyg.config.js',
            f'trumbowyg/dist/trumbowyg{min_js}.js',
            f'trumbowyg/dist/plugins/upload/trumbowyg.upload{min_js}.js',
            'admin/js/trumbowyg.config.js',
        ]

        lang = get_trumbowyg_language(get_language())
        if lang:
            js.append('trumbowyg/dist/langs/{}.js'.format(lang))

        return css, js + highlight_js(getattr(django_settings, 'DEBUG', False))


class RichTextField(forms.CharField):
    """
    A text field with a rich text editor.

    This class does two main things:
    - add a css class to trigger the rich js text editor
    - sanitize the generated html
    """

    def __init__(self, *args, widget=None, **kwargs):
        """Init RichTextField with widget and CSS class."""
        widget = widget or TrumbowygWidget
        self.css_class = kwargs.pop('css_class', 'textarea-wysiwyg')

        super().__init__(*args, widget=widget, **kwargs)

    def widget_attrs(self, widget):
        """Add a custom css class to the widget."""
        attrs = super().widget_attrs(widget)
        attrs.update({
            'class': self.css_class,
        })

        return attrs
