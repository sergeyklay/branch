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

from django.views.generic import ListView, DateDetailView

from apps.website.models import Setting
from .models import Post


class PageDetailsMixin:
    """Pass a defined title to context"""

    description = None
    title = None

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = self.get_title()
        if title:
            context['page_title'] = self.get_title()

        description = self.get_description()
        if description:
            context['page_description'] = self.get_description()

        return context


class PostDetailView(PageDetailsMixin, DateDetailView):
    model = Post
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'blog/posts/view.html'
    queryset = Post.published.all()

    def get_title(self):
        if getattr(self.object, 'meta_title', None):
            return self.object.meta_title

        if getattr(self.object, 'title', None):
            return self.object.title

        return None

    def get_description(self):
        if getattr(self.object, 'meta_description', None):
            return self.object.meta_description

        if getattr(self.object, 'excerpt', None):
            return self.object.excerpt

        return None


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = Setting.website.get('pagination_per_page', 5)
    template_name = 'blog/posts/list.html'
