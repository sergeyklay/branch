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

"""The top-level module for branch package.

This module tracks the version of the package as well as the base
package info used by various functions within Branch.

Variables:

    celery_app

Misc variables:

    __copyright__
    __version__
    __license__
    __author__
    __author_email__
    __url__
    __description__

Refer to the `documentation <https://github.com/sergeyklay/branch/>`_
for details on the use of this package.

"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)

__copyright__ = 'Copyright (C) 2021 Serghei Iakovlev'
__version__ = '1.3.0'
__license__ = 'GPLv3+'
__author__ = 'Serghei Iakovlev'
__author_email__ = 'egrep@protonmail.ch'
__url__ = 'https://github.com/sergeyklay/branch'
__description__ = 'A Django blog application with features of a standard blogging platform.'  # noqa
