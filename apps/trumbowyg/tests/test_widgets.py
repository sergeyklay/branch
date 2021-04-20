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


from django.conf import settings
from django.utils.translation import trans_real

from apps.trumbowyg.widgets import AdminTrumbowygWidget


def test_admin_trumbowyg_widget_custom_lang(monkeypatch):
    widget = AdminTrumbowygWidget()

    trans_real.deactivate()
    monkeypatch.setattr(settings, 'LANGUAGE_CODE', 'ru')

    _, js = widget.assets

    assert 'trumbowyg/dist/langs/ru.js' in js
    assert 'trumbowyg/dist/langs/en.js' not in js


def test_admin_trumbowyg_widget_en_lang(monkeypatch):
    widget = AdminTrumbowygWidget()

    trans_real.deactivate()
    monkeypatch.setattr(settings, 'LANGUAGE_CODE', 'en')

    _, js = widget.assets

    assert 'trumbowyg/dist/langs/en.js' not in js
