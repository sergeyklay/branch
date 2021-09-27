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

"""Provides tools to prepare project to use for production environment."""

import time
import uuid
from datetime import datetime

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Generate project-wide constants."""

    help = 'Generate project-wide constants.'

    def __init__(self, stdout=None, stderr=None, no_color=False,
                 force_color=False):
        """Init command with empty build_id."""
        super().__init__(stdout, stderr, no_color, force_color)
        self.build_id = None

    def update_build_info(self):
        """Regenerate project build info."""
        time_hash = hex(int(time.time()))
        build_id = uuid.uuid4().hex
        self.build_id = f'{build_id[:8]}-{time_hash[2:]}'

    def handle(self, *args, **kwargs):
        """Store project-wide constants in build.py file."""
        self.update_build_info()
        build_id_file = settings.BASE_DIR / 'build.py'
        build_date_short = datetime.utcnow().strftime('%Y-%m-%d')

        with open(build_id_file, 'w', encoding='utf-8') as file:
            file.write(f'BUILD_ID = "{self.build_id}"\n')
            file.write(f'BUILD_ID_SHORT = "{self.build_id[:4]}"\n')
            file.write(f'BUILD_DATE_SHORT = "{build_date_short}"\n')

            site = get_current_site(request=None)
            file.write(f'DOMAIN = "{site.domain}"\n')
