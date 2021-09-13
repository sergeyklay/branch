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

"""Comments URL Configuration.

This configuration will replace the original one from django_comments.urls,
removing the following features:

    - comments-approve
    - comments-approve-done
    - comments-delete
    - comments-delete-done
    - comments-flag
    - comments-flag-done

This is not in demand right now, so disabled.

"""

from django.contrib.contenttypes.views import shortcut
from django.urls import path, re_path
from django_comments.views.comments import comment_done, post_comment

urlpatterns = [
    path('post/', post_comment, name='comments-post-comment'),
    path('posted/', comment_done, name='comments-comment-done'),

    re_path(r'^cr/(\d+)/(.+)/$', shortcut, name='comments-url-redirect'),
]
