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

import os

from django.conf import settings
from django.utils import translation


def test_language_file_integrity():
    """Confirm that translation files are in a good state."""
    for locale in os.listdir(settings.BASE_DIR / 'locales'):
        # Attempt translation activation to confirm that the
        # language files are working
        with translation.override(locale):
            pass
