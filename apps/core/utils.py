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

"""Common utils for the whole project."""

from contextlib import contextmanager
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import activate, get_language
from django.utils.translation import trans_real


@contextmanager
def override_language(language):
    """Temporarily override language with a context manager."""
    cur_language = get_language()
    activate(language)
    yield
    activate(cur_language)


def to_absolute_url(url, site=None):
    """Take an URL and prepend the SITE_URL."""
    if url and url.startswith(('http://', 'https://', 'mailto:')):
        return url

    return urljoin(site or settings.SITE_URL, url)


def to_language(locale):
    """Like Django's to_language, but en_US comes out as en-US."""
    if '_' in locale:
        return to_language(trans_real.to_language(locale))

    if '-' in locale:
        idx = locale.find('-')
        return locale[:idx].lower() + '-' + locale[idx + 1:].upper()

    return trans_real.to_language(locale)
