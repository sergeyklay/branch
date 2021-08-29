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

"""Locale aware middlewares and related functionality."""

from contextlib import suppress

from django.conf import settings


def inject_accept_language(get_response):
    """
    Ignore Accept-Language HTTP headers.

    This will force the I18N machinery to always choose

    - SITE_LANGUAGE_CODE for the main site
    - ADMIN_LANGUAGE_CODE for the admin site

    as the default initial language unless another one is set via
    sessions or cookies.

    Should be installed *before* any middleware that checks
    request.META['HTTP_ACCEPT_LANGUAGE'], namely
    `django.middleware.locale.LocaleMiddleware`.
    """
    def middleware(request):
        if request.path.startswith(f'{settings.ADMIN_SITE_URL}/'):
            lang = settings.ADMIN_LANGUAGE_CODE
        else:
            lang = settings.SITE_LANGUAGE_CODE

        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')
        with suppress(ValueError):
            # Remove `lang` from the HTTP_ACCEPT_LANGUAGE to avoid duplicates
            accept.remove(lang)

        accept = [lang] + accept
        request.META['HTTP_ACCEPT_LANGUAGE'] = f"{','.join(accept)}"
        return get_response(request)

    return middleware
