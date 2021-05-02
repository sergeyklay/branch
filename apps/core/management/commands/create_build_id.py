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

from django.core.management.base import BaseCommand
import time
import uuid
from django.conf import settings


class Command(BaseCommand):
    help = "Generate project's build id"

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.build_id = None

    def update_build_info(self):
        time_hash = hex(int(time.time()))
        build_id = uuid.uuid4().hex

        self.build_id = '%s-%s' % (build_id[:8], time_hash[2:])

    def handle(self, *args, **kwargs):
        self.update_build_info()
        build_id_file = settings.BASE_DIR('build.py')
        with open(build_id_file, 'w') as f:
            f.write('BUILD_ID = "%s"\n' % self.build_id)
