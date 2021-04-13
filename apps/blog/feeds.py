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

"""Blog feed module."""

import datetime

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from django.utils import feedgenerator
from django.utils.html import escape, strip_tags

from apps.website.models import Setting
from .models import Post


class PostsFeedRSS(Feed):
    """This represents RSS feed for blog posts."""

    link = reverse_lazy('blog:post_list')

    feed_limit = 20
    words_limit = 30

    def __init__(self):
        self._site = Site.objects.get(pk=settings.SITE_ID)
        self._copyright_holder = Setting.website.get('copyright_holder')

    def title(self):
        """Return the feed's title as a normal Python string."""
        return self._site.name

    def description(self):
        """Return the feed's description as a normal Python string."""
        description = Setting.website.get('description')
        return description

    def author_name(self):
        """Return the feed's author's name as a normal Python string."""
        return self._copyright_holder or 'Branch'

    def author_email(self):
        """Return the feed's author's email as a normal Python string."""
        return Setting.website.get('contact_email')

    def feed_copyright(self):
        """Return the feed's copyright notice as a normal Python string."""
        now = datetime.datetime.now()
        copyright_holder = self._copyright_holder or 'Branch'
        return f'Copyright (c) 2018-{now.year} {copyright_holder}'

    def items(self):
        """Return a list of items to publish in this feed."""
        return Post.published.all()[:self.feed_limit]

    def item_title(self, item):
        """
        Take an item, as returned by items(), and return the item's
        title as a normal Python string.
        """
        # Titles should be double escaped by default (see #6533)
        return escape(item.title)

    def item_description(self, item):
        """
        Take an item, as returned by items(), and return the item's
        description as a normal Python string.
        """
        excerpt = item.excerpt or item.body
        return truncatewords(strip_tags(excerpt), self.words_limit)

    def item_author_name(self, item):
        """
        Take an item, as returned by items(), and return the item's
        author's name as a normal Python string.
        """
        return item.author.get_full_name()

    def item_author_email(self, item):
        """
        Take an item, as returned by items(), and return the item's
        author's email as a normal Python string.
        """
        return item.author.email

    def item_pubdate(self, item):
        """
        Take an item, as returned by items(), and return the item's
        pubdate.
        """
        return item.published_at

    def item_updateddate(self, item):
        """
        Take an item, as returned by items(), and return the item's
        updateddate.
        """
        return item.updated_at


class PostsFeedAtom(PostsFeedRSS):
    """This represents Atom feed for blog posts."""

    feed_type = feedgenerator.Atom1Feed

    def subtitle(self):
        """Return the feed's subtitle as a normal Python string."""
        return self.description()

    def item_description(self, item):
        """
        Take an item, as returned by items(), and return the item's
        description as a normal Python string.
        """
        excerpt = item.excerpt
        if not excerpt or len(excerpt) == 0:
            excerpt = truncatewords(strip_tags(item.body), self.words_limit)

        return excerpt
