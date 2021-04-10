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

# The socket to bind.
bind = 'unix:/run/branch.sock'

# Workers silent for more than this many seconds are killed and restarted.
timeout = 60

# The Access log file to write to.
accesslog = '/var/log/gunicorn/branch.access.log'

# The Error log file to write to.
errorlog = '/var/log/gunicorn/branch.error.log'

# The number of worker processes for handling requests.
workers = 3
