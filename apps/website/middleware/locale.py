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

"""Website locale middleware modules."""

from contextlib import suppress

from django.conf import settings

from apps.core.utils import admin_path


def inject_accept_language(get_response):
    """
    Ignore Accept-Language HTTP headers.

    This will force the I18N machinery to always choose

      - DEFAULT_LANGUAGE_CODE for the main site
      - ADMIN_LANGUAGE_CODE for the admin site

    as the default initial language unless another one is set via
    sessions or cookies.

    Should be installed before any middleware that checks
    request.META['HTTP_ACCEPT_LANGUAGE'], namely
    `django.middleware.locale.LocaleMiddleware`.
    """
    admin_url = f'/{admin_path()}'
    admin_lang = getattr(settings, 'ADMIN_LANGUAGE_CODE',
                         settings.LANGUAGE_CODE)
    def_lang = getattr(settings, 'DEFAULT_LANGUAGE_CODE',
                       settings.LANGUAGE_CODE)

    def middleware(request):
        # Force default locale for the main site
        lang = admin_lang if request.path.startswith(admin_url) else def_lang
        accept = request.META.get('HTTP_ACCEPT_LANGUAGE', '').split(',')

        with suppress(ValueError):
            # Remove `lang` from the HTTP_ACCEPT_LANGUAGE to avoid duplicates
            accept.remove(lang)

        accept = [lang] + accept
        request.META['HTTP_ACCEPT_LANGUAGE'] = f"""{','.join(accept)}"""
        return get_response(request)

    return middleware
