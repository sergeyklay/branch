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

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DateDetailView, ListView
from taggit.models import Tag

from apps.seo.mixins import PageDetailsMixin
from .models import Post


class PostDetailView(PageDetailsMixin, DateDetailView):
    """Display a blog post detail."""

    model = Post
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    template_name = 'blog/posts/view.html'

    @property
    def title(self):
        """Get the title of the current post."""
        if self.object.meta_title:
            return self.object.meta_title

        if self.object.title:
            return self.object.title

        return None

    @property
    def description(self):
        """Get the description of the current post."""
        if self.object.meta_description:
            return self.object.meta_description

        if self.object.excerpt:
            return self.object.excerpt

        return settings.SITE_DESCRIPTION

    @property
    def author(self):
        """Get the author of the current post."""
        return self.object.author.get_full_name()

    @property
    def locale(self):
        """Get the locale of the current post."""
        return self.object.locale

    @property
    def resource_type(self):
        """Get the type of the current post."""
        return self.object.post_type

    def get_success_url(self):
        """Get the URL to redirect to when a form is successfully validated."""
        return f'{self.object.get_absolute_url()}#feedback-message'

    def get_queryset(self):
        """Return the `QuerySet` that will be used to look up the blog post."""
        return Post.published.all()

    def get_context_data(self, **kwargs):
        """Get post's context data to use in template."""
        context = super().get_context_data(**kwargs)
        context['next'] = self.get_success_url()
        return context


class PostListView(ListView):
    """Display the list of published blog posts."""

    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/posts/list.html'

    def get_paginate_by(self, queryset):
        """Get the number of items to paginate by."""
        return settings.PAGE_SIZE


class PostTaggedView(ListView):
    """Display the list of published blog posts tagged by specific tag."""

    context_object_name = 'posts'
    template_name = 'blog/posts/list.html'

    def get_queryset(self):
        """Return the `QuerySet` that will be used to look up the blog post."""
        # TODO: Duplicate query in get_context_data()
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.published.filter(tags__in=[tag])

    def get_paginate_by(self, queryset):
        """Get the number of items to paginate by."""
        return settings.PAGE_SIZE

    def get_context_data(self, *, object_list=None, **kwargs):
        """Get post's context data to use in template."""
        context = super().get_context_data(**kwargs)
        # TODO: Duplicate query in get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])

        context.update({
            'tagged': tag.name,
            'resource_type': 'website',
            'seo_author': settings.SITE_NAME,
            'seo_title': _('Posts tagged [{ tag }]') % {'tag': tag.name},
            'resource_url': reverse(
                'blog:post_list_by_tag',
                args=(self.kwargs['slug'],)
            ),
        })

        return context
