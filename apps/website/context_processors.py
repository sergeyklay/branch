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

"""Website context processors."""

from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import get_language, gettext_lazy, to_locale

from .models import Setting


def app_settings(request):  # pylint: disable=unused-argument
    """Add global website settings to the context."""
    context_extras = {}

    for obj in Setting.objects.all():
        context_extras[f'site_{obj.name}'] = obj.value

    return context_extras


def base_url(request):
    """Add website base URL and its name to the context."""
    current_site = get_current_site(request)
    scheme = 'https://' if request.is_secure() else 'http://'

    return {
        'BASE_URL': scheme + current_site.domain,
        'SITE_NAME': gettext_lazy(current_site.name),
    }


def locale(_):
    """Add current locale to the context."""
    return {'LOCALE': to_locale(get_language())}
