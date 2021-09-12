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

"""The top-level module for comments application.

This is an add-on over the Django Comments Framework to provide the
features the blog needs.

"""


def get_form():
    """
    Return the form comments class.

    Returned form class will be used for creating, validating, and saving
    blog's comment model.
    """
    from apps.comments.forms import PostCommentForm
    return PostCommentForm
