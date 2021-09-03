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
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DateDetailView, ListView
from django.views.generic.edit import FormMixin
from taggit.models import Tag

from apps.seo.mixins import PageDetailsMixin
from .forms import CommentForm
from .models import Post


class PostDetailView(PageDetailsMixin, FormMixin, DateDetailView):
    """Display a blog post detail."""

    model = Post
    context_object_name = 'post'
    date_field = 'published_at'
    month_format = '%m'
    form_class = CommentForm
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

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests.

        Set instance object, instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """Get post's context data to use in template."""
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(status='published')
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        """
        If the form is valid, redirect to get_success_url().

        This method is called when valid form data has been POSTed.
        It will return an HttpResponse.
        """
        # Assign current post to a new comment before save
        form.instance.post = self.object
        form.save()

        response = super().form_valid(form)

        success_message = _('Your comment has been sent for moderation. '
                            'This means comment will "held" until I okays it '
                            'and publish it.')
        messages.success(self.request, success_message)

        return response


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
