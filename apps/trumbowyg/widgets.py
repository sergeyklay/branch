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
from django.conf import settings
from django.contrib.admin import widgets


def highlight_js():
    """Perform manipulation of asset paths to enable code highlight."""
    components = (
        'abnf', 'antlr4', 'apacheconf',
        'bash', 'bison', 'bnf',
        'c', 'cpp',
        'diff',
        'ebnf',
        'python',
    )

    trumbowyg_plugins = 'trumbowyg/dist/plugins'
    prefix = 'prismjs/components/prism'
    suffix = f"{'' if settings.DEBUG else '.min'}"

    trumbowyg_base = f'{trumbowyg_plugins}/highlight/trumbowyg.highlight'
    trumbowyg = f"{trumbowyg_base}{'' if settings.DEBUG else '.min'}.js"

    result = map(lambda c: f'{prefix}-{c}{suffix}.js', components)
    return ('prismjs/prism.js',) + tuple(result) + (trumbowyg,)


class TrumbowygWidget(forms.Textarea):
    """
    Widget class to add a Trumbowyg instance on a textarea.

    Take the same arguments than ``forms.Textarea``.
    """

    template_name = 'trumbowyg/forms/widgets/textarea.html'

    @property
    def assets(self):
        """Setup static assets to use in WYSIWYG editor."""
        css = (
            'prismjs/themes/prism.css',
            'trumbowyg/dist/ui/trumbowyg{}.css'.format(
                '' if settings.DEBUG else '.min',
            ),
            'trumbowyg/dist/plugins/highlight/ui/trumbowyg.highlight{}.css'.format(  # noqa
                '' if settings.DEBUG else '.min',
            ),
        )

        js = (
            'trumbowyg/js/trumbowyg.config.js',
            'trumbowyg/dist/trumbowyg{}.js'.format(
                '' if settings.DEBUG else '.min',
            ),
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

    Acts like ``TrumbowygWidget`` but enables aditional plugins.
    """

    @property
    def assets(self):
        """Setup static assets to use in WYSIWYG editor."""
        css, _ = super().assets

        js = (
            'admin/js/jquery.init.js',
            'trumbowyg/js/trumbowyg.config.js',
            'trumbowyg/dist/trumbowyg{}.js'.format(
                '' if settings.DEBUG else '.min'
            ),
            'trumbowyg/dist/plugins/upload/trumbowyg.upload{}.js'.format(
                '' if settings.DEBUG else '.min'
            ),
            'admin/js/trumbowyg.config.js',
        )

        return css, js + highlight_js()


class RichTextField(forms.CharField):
    """
    A text field with a rich text editor.

    This class does two main things:
    - add a css class to trigger the rich js text editor
    - sanitize the generated html
    """

    def __init__(self, *args, widget=None, **kwargs):
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
