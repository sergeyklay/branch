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

"""branch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .utils import admin_path

urlpatterns = [
    path('', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.telegraph.urls', namespace='telegraph')),
    path('', include('apps.pages.urls', namespace='pages')),
    path(f'{admin_path()}/', admin.site.urls),
]

if settings.DEBUG:
    from django.urls import re_path
    from django.views.static import serve
    import debug_toolbar
    import os

    # Static & media files for development environment
    static_routes = [
        re_path(
            r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), serve, {
                'document_root': settings.STATIC_ROOT
            }
        ),
        re_path(
            r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), serve, {
                'document_root': settings.MEDIA_ROOT
            }
        )
    ]

    icons = [
        # Some browsers requests for icons from the site root, despite meta
        # tags definition.
        re_path(
            r'^(?P<path>favicon\.ico|apple-touch-icon.*\.png)$', serve, {
                'document_root': f'{settings.STATIC_ROOT}/icons',
            },
        ),

        # The following action icons are hardcoded in Django source code
        #
        # '../img/icon-viewlink.svg'
        # '../img/icon-addlink.svg'
        # '../img/icon-changelink.svg'
        # '../img/icon-deletelink.svg
        #
        # When opening '/admin/<APP>/<MODEL>/' Safari makes
        # request to the following URLS '/admin/<APP>/<MODEL>/img/icon-.*.svg'
        #
        # For more see:
        # /django/contrib/admin/static/admin/css/base.css
        # https://discussions.apple.com/thread/1407049
        re_path(r'^.*/(?P<path>img/icon-.*.svg)$', serve, {
            'document_root': os.path.join(settings.STATIC_ROOT, 'admin'),
        }),
    ]

    debug = [
        path('__debug__/', include(debug_toolbar.urls))
    ]

    urlpatterns = static_routes + icons + debug + urlpatterns
