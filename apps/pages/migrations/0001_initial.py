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

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
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
                    'title',
                    models.CharField(
                        max_length=250,
                        verbose_name='Title',
                    )
                ),
                (
                    'slug',
                    models.SlugField(
                        help_text='Let it empty so it will be autopopulated.',
                        max_length=250,
                        unique_for_date='published_at',
                        verbose_name='Slug',
                    )
                ),
                (
                    'no_index',
                    models.BooleanField(
                        default=False,
                        help_text=('Prevent this page from appearing '
                                   'in search index'),
                        verbose_name='Block search indexing',
                    )
                ),
                (
                    'body',
                    models.TextField(
                        verbose_name='Full text of the post',
                    )
                ),
                (
                    'published_at',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='First publication date',
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Date created',
                    )
                ),
                (
                    'updated_at',
                    models.DateTimeField(
                        auto_now=True,
                        verbose_name='Date updated',
                    )
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('draft', 'Draft'),
                            ('published', 'Published'),
                        ],
                        default='draft',
                        max_length=10,
                        verbose_name='Status',
                    )
                ),
                (
                    'meta_title',
                    models.CharField(
                        blank=True,
                        default='',
                        help_text=('This will be displayed in meta tags. '
                                   'Keep it under 60 characters. Leave empty '
                                   "and the post's title will be used."),
                        max_length=60,
                        verbose_name='Meta title',
                    )
                ),
                (
                    'meta_description',
                    models.TextField(
                        blank=True,
                        default='',
                        help_text=('This will be displayed in meta tags. '
                                   'Keep it under 120 characters.'),
                        max_length=256,
                        verbose_name='Meta description',
                    )
                ),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ('title',),
            },
        ),
    ]
