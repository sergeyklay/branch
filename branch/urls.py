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

"""branch URL Configuration."""

import os

from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from apps.blog.sitemaps import PostSitemap, PostsListSitemap  # noqa: I100
from apps.pages.sitemaps import PageSitemap  # noqa: I100,I201
from apps.telegraph.sitemaps import TelegraphSitemap  # noqa: I100,I201
from .utils import admin_path


def sitemaps():
    """Get whole website sitemap."""
    return {'sitemaps': {
        'page': PageSitemap,
        'telegraph': TelegraphSitemap,
        'post': PostSitemap,
        'post_list': PostsListSitemap,
    }}


urlpatterns = [
    path('', include('apps.blog.urls', namespace='blog')),
    path('', include('apps.telegraph.urls', namespace='telegraph')),
    path('', include('apps.pages.urls', namespace='pages')),
    path(f'{admin_path()}/', admin.site.urls),
    path('sitemap.xml', sitemap, sitemaps(), name='sitemap'),
]

if settings.DEBUG:
    import debug_toolbar

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
        # And when sending requests to '/<ADMIN_URL>/<APP>/<MODEL>/', Safari
        # makes request to the following URLS
        # '/<ADMIN_URL>/<MODEL>/img/icon-.*.svg' due to relative nature of
        # links.
        #
        # For more see:
        #    - django/contrib/admin/static/admin/css/base.css
        #    - https://discussions.apple.com/thread/1407049
        #
        re_path(r'^.*/(?P<path>img/icon-.*.svg)$', serve, {
            'document_root': os.path.join(settings.STATIC_ROOT, 'admin'),
        }),
    ]

    debug = [
        path('__debug__/', include(debug_toolbar.urls))
    ]

    urlpatterns = static_routes + icons + debug + urlpatterns

# TODO: Handle 5xx
handler404 = 'apps.website.views.error_404'
