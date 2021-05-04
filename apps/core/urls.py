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

"""A configuration for shared URLs."""

from django.urls import re_path

from .utils import is_prod_like_environment
from .views import handler404, handler500, humans, robots

app_name = 'core'  # pylint: disable=invalid-name

urlpatterns = (
    re_path(r'^humans\.txt$', humans, name='humans.txt'),
    re_path(r'^robots\.txt$', robots, name='robots.txt'),
)

# The URL configuration bellow is needed for testing and local development.
if not is_prod_like_environment():
    urlpatterns = (
        re_path(r'^404/?$', handler404),
        re_path(r'^500/?$', handler500),
    ) + urlpatterns
