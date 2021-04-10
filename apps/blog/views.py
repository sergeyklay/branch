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

"""Blog views definitions."""

from django.views.generic import DateDetailView, ListView

from apps.website.models import Setting
from branch.mixins import PageDetailsMixin
from .models import Post


class PostDetailView(PageDetailsMixin, DateDetailView):
    """Display a blog post detail."""

    model = Post
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'blog/posts/view.html'
    queryset = Post.published.all()

    @property
    def title(self):
        if self.object.meta_title:
            return self.object.meta_title

        if self.object.title:
            return self.object.title

        return None

    @property
    def description(self):
        if self.object.meta_description:
            return self.object.meta_description

        if self.object.excerpt:
            return self.object.excerpt

        return None

    @property
    def author(self):
        return self.object.author.get_full_name()

    @property
    def locale(self):
        return self.object.locale

    @property
    def type(self):
        return self.object.type


class PostListView(ListView):
    """Display the list of published blog posts."""

    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/posts/list.html'

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by.
        """
        return Setting.website.get('pagination_per_page', 5)
