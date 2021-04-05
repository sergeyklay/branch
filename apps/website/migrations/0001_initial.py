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


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'name',
                    models.CharField(
                        db_index=True,
                        help_text='Name of site-wide variable',
                        max_length=200,
                        verbose_name='Setting name',
                    )
                ),
                (
                    'value',
                    models.TextField(
                        blank=True,
                        help_text=('Value of site-wide variable '
                                   'that scripts can reference'),
                        max_length=250,
                        null=True,
                        verbose_name='Setting value',
                    )
                ),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
                'ordering': ('name',),
            },
        ),
    ]
