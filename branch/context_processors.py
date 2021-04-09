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

"""Common context processors."""

from django.conf import settings
from django.utils.translation import get_language, to_locale


def base_url(request):
    """Return a BASE_URL template context for the current request."""

    if getattr(settings, 'BASE_URL', None):
        return {'BASE_URL': settings.BASE_URL}

    scheme = 'https://' if request.is_secure() else 'http://'
    return {'BASE_URL': scheme + request.get_host()}


def locale(_):
    """Return current resource locale as well as all alternate locales."""
    current_lang = get_language()
    current_locale = to_locale(current_lang)

    context = {'LOCALE': current_locale}
    locales = []

    for lang in getattr(settings, 'LANGUAGES', []):
        if len(lang) == 0 or lang[0] == current_lang:
            continue
        locales.append(to_locale(lang[0]))

    context['ALT_LOCALES'] = locales

    return context
