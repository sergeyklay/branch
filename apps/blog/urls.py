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

"""Blog URL Configuration."""

from django.urls import path

from . import views
from .feeds import PostsFeedAtom, PostsFeedRSS

app_name = 'blog'  # pylint: disable=invalid-name

urlpatterns = (
    path('', views.PostListView.as_view(), name='post_list'),
    path('atom.xml', PostsFeedAtom(), name='post_atom'),
    path('rss.xml', PostsFeedRSS(), name='post_rss'),
    path(
        'post/<int:year>/<int:month>/<int:day>/<slug:slug>.html',
        views.PostDetailView.as_view(),
        name='post_view'
    ),
)
