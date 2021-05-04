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

"""Common views definitions."""

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string


def robots(request):
    """Generate a robots.txt"""
    if not settings.ALLOW_ROBOTS:
        content = 'User-agent: *\nDisallow: /'
    else:
        content = render_to_string(
            'core/robots.html',
            request=request,
            context={'domain': settings.DOMAIN},
        )

    return HttpResponse(content, content_type='text/plain')


def humans(request):
    """Generate a humans.txt"""
    content = render_to_string(
        'core/humans.html',
        request=request,
        context={
            'domain': settings.DOMAIN,
            'build_date': settings.BUILD_DATE_SHORT,
        },
    )

    return HttpResponse(content, content_type='text/plain; charset=utf-8')
