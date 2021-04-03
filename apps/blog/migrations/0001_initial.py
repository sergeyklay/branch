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
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
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
                        max_length=250,
                        unique_for_date='published_at',
                        verbose_name='Slug',
                    )
                ),
                (
                    'body',
                    models.TextField(
                        verbose_name='Content',
                    )
                ),
                (
                    'published_at',
                    models.DateTimeField(
                        default=django.utils.timezone.now,
                        verbose_name='Published at',
                    )
                ),
                (
                    'created_at',
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name='Created at',
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
                    'author',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='posts',
                        to=settings.AUTH_USER_MODEL,
                        verbose_name='Author',
                    )
                ),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ('-published_at',),
            },
        ),
    ]
