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
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.utils.html import escape, strip_tags
from django.utils.text import format_lazy
from django.utils.translation import pgettext_lazy

from apps.core.utils import to_absolute_url
from .models import Post


class LatestPostsFeedRSS(Feed):
    """This represents RSS feed for blog posts."""

    feed_type = Rss201rev2Feed

    def link(self):
        """Get link for the feed as a whole."""
        return to_absolute_url(reverse('blog:posts_rss'))

    def title(self):
        """Get title for the feed as a whole."""
        feed_title = pgettext_lazy('feed title', 'Latest posts')
        return format_lazy(
            '{feed_title} - {site_name}',
            feed_title=feed_title,
            site_name=settings.SITE_NAME,
        )

    def description(self):
        """Return the feed's description as a normal Python string."""
        return settings.SITE_DESCRIPTION

    def author_name(self):
        """Return the feed's author's name as a normal Python string."""
        return settings.COPYRIGHT_HOLDER

    def author_email(self):
        """Return the feed's author's email as a normal Python string."""
        return settings.CONTACT_EMAIL

    def feed_copyright(self):
        """Return the feed's copyright notice as a normal Python string."""
        now = datetime.datetime.now()
        copyright_holder = self.author_name()
        return f'Copyright (c) 2018-{now.year} {copyright_holder}'

    def items(self):
        """Return a list of items to publish in this feed."""
        feed_limit = getattr(settings, 'FEED_MAX_ITEMS', 20)
        return Post.published.all()[:feed_limit]

    def item_title(self, item):
        """
        Get the given item title.

        Take an item, as returned by items(), and return the item's
        title as a normal Python string.
        """
        # Titles should be double escaped by default (see #6533)
        return escape(item.title)

    def item_link(self, item):
        """
        Get the given item absolute URL.

        Takes an item, as returned by items(), and returns the item's URL.
        """
        return to_absolute_url(item.get_absolute_url())

    def item_description(self, item):
        """
        Get the given item description.

        Take an item, as returned by items(), and return the item's
        description as a normal Python string.
        """
        paragraph = item.excerpt
        if not paragraph or len(paragraph) == 0:
            paragraph = strip_tags(item.body)

        words_limit = getattr(settings, 'FEED_WORD_LIMIT', 50)
        return truncatewords(strip_tags(paragraph), words_limit)

    def item_author_name(self, item):
        """
        Get the given item author name.

        Take an item, as returned by items(), and return the item's
        author's name as a normal Python string.
        """
        return item.author.get_full_name()

    def item_author_email(self, item):
        """
        Get the given item author email.

        Take an item, as returned by items(), and return the item's
        author's email as a normal Python string.
        """
        return item.author.email

    def item_pubdate(self, item):
        """
        Get the given item published date.

        Take an item, as returned by items(), and return the item's
        pubdate.
        """
        return item.published_at


class LatestPostsFeedAtom(LatestPostsFeedRSS):
    """This represents Atom feed for blog posts."""

    feed_type = Atom1Feed

    def link(self):
        """Get link for the feed as a whole."""
        return to_absolute_url(reverse('blog:posts_atom'))

    def subtitle(self):
        """Return the feed's subtitle as a normal Python string."""
        return self.description()

    def item_updateddate(self, item):
        """
        Get the given item updated date.

        Take an item, as returned by items(), and return the item's
        updateddate.
        """
        return item.updated_at
