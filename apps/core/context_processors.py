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

"""Blog-wide context processors."""

from django.conf import settings
from django.utils.translation import get_language, get_language_bidi, to_locale


def base_url(request):
    """Add website base URL and its name to the context."""
    return {
        'BASE_URL': settings.BASE_URL,
    }


def i18n(request):
    """Add current locale and language settings to the context."""
    lang = get_language()
    return {
        'LANGUAGES': settings.LANGUAGES,
        'LANG_CODE': f'{settings.LANGUAGE_CODE}'[:2],
        'LANG': settings.LANGUAGE_URL_MAP.get(lang, lang),
        'LOCALE': to_locale(get_language()),
        'DIR': 'rtl' if get_language_bidi() else 'ltr',
    }


def global_settings(request):
    """Storing standard blog-wide information used in templates."""
    context = {}

    context.update(
        {
            'settings': settings,
        }
    )

    return context
