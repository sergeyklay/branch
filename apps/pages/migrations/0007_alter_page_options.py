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

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_alter_page_locale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={
                'ordering': ('title',),
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
    ]
