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

"""Provides wrapper for 'makemessages' command."""

from django.core.management import call_command
from django.core.management.commands.makemessages import (
    Command as MakeMessagesCommand
)


class Command(MakeMessagesCommand):
    """Automates the creation and upkeep of message files."""

    help = MakeMessagesCommand.help + (
        '\nThis command ignores storage directory by default.'
    )

    def handle(self, *args, **options):
        """Execute 'makemessages' command."""
        if 'ignore_patterns' not in options:
            options['ignore_patterns'] = []

        options['ignore_patterns'] += ['storage*']
        call_command('makemessages', **options)
