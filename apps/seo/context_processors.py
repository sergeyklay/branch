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

"""SEO-related context processors."""

from django.conf import settings


def google_analytics(request):
    """Add GA Tracking ID and search keywords to the context."""
    return {
        'GA_TRACKING_ID': getattr(settings, 'GA_TRACKING_ID', ''),
        'SEO_KEYWORDS': getattr(settings, 'SEO_KEYWORDS', ''),
    }
