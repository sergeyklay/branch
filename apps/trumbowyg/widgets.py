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
    """Perform manipulation of asset paths to enable highlight."""
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

    def __init__(self, attrs=None):
        super().__init__(attrs)
        self.suffix = '' if getattr(settings, 'DEBUG', False) else '.min'

    @property
    def assets(self):
        """Setup static assets to use in WYSIWYG editor."""
        tw_dist = 'trumbowyg/dist'
        tw_plugins = f'{tw_dist}/plugins'

        css = (
            'prismjs/themes/prism.css',
            f'{tw_dist}/ui/trumbowyg{self.suffix}.css',
            f'{tw_plugins}/highlight/ui/trumbowyg.highlight{self.suffix}.css',
        )

        js = (
            'trumbowyg/js/trumbowyg.config.js',
            f'{tw_dist}/trumbowyg{self.suffix}.js',
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
        tw_dist = 'trumbowyg/dist'
        tw_plugins = f'{tw_dist}/plugins'

        css, _ = super().assets

        js = (
            'admin/js/jquery.init.js',
            'trumbowyg/js/trumbowyg.config.js',
            f'{tw_dist}/trumbowyg{self.suffix}.js',
            f'{tw_plugins}/upload/trumbowyg.upload{self.suffix}.js',
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
