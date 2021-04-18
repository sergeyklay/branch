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

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_alter_page_no_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name='Date created',
            ),
        ),
        migrations.AlterField(
            model_name='page',
            name='updated_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name='Date updated',
            ),
        ),
    ]
