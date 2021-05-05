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

"""Production Django settings for branch project."""

# pylint: disable-msg=w0614,w0401
from .base import *  # noqa

# SECURITY WARNING: define the correct hosts in production
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# A list of IP addresses, as strings, that:
# - Allow the debug() context processor to add some variables to the template
#   context.
# - Can use the admindocs bookmarklets even if not logged in as a staff user.
# - Are marked as “internal” in AdminEmailHandler emails.
INTERNAL_IPS = env.list('INTERNAL_IPS')

COMPRESS_OFFLINE = True

# Redirect all non-HTTPS requests to HTTPS (except for those URLs matching a
# regular expression listed in SECURE_REDIRECT_EXEMPT).
SECURE_SSL_REDIRECT = True

# Add the 'includeSubDomains' directive to the HTTP Strict Transport Security
# header.
SECURE_HSTS_SECONDS = 3600

# Add the 'includeSubDomains' directive to the HTTP Strict Transport Security
# header.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Add the 'preload' directive to the HTTP Strict Transport Security header.
SECURE_HSTS_PRELOAD = True

# Whether to use a secure cookie for the session cookie. If this is set to
# True, the cookie will be marked as “secure”, which means browsers may ensure
# that the cookie is only sent under an HTTPS connection.
SESSION_COOKIE_SECURE = True

# Whether to use a secure cookie for the CSRF cookie. If this is set to True,
# the cookie will be marked as “secure”, which means browsers may ensure that
# the cookie is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True
