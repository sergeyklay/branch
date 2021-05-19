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
from django.template import loader
from django.views.defaults import page_not_found, server_error


def robots(request):
    """Generate a robots.txt file."""
    if not settings.ALLOW_ROBOTS:
        body = 'User-agent: *\nDisallow: /'
    else:
        template = loader.get_template('core/robots.html')
        body = template.render({'domain': settings.DOMAIN}, request)

    return HttpResponse(body, content_type='text/plain; charset=utf-8')


def humans(request):
    """Generate a humans.txt file."""
    template = loader.get_template('core/humans.html')
    context = {'build_date': settings.BUILD_DATE_SHORT}
    body = template.render(context, request)

    return HttpResponse(body, content_type='text/plain; charset=utf-8')


def handler404(request, exception=None, **kwargs):
    """Site-wide 404 handler."""
    return page_not_found(
        request=request,
        exception=exception,
        template_name='core/404.html',
    )


def handler500(request, **kwargs):
    """Site-wide 500 handler."""
    return server_error(
        request=request,
        template_name='core/500.html'
    )
