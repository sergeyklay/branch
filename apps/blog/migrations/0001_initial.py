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
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')
                 ),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(
                    max_length=250,
                    unique_for_date='publish')
                 ),
                ('body', models.TextField()),
                ('published', models.DateTimeField(
                    default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(
                    choices=[
                        ('draft', 'Draft'),
                        ('published', 'Published'),
                    ],
                    default='draft',
                    max_length=10)
                 ),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='posts',
                    to=settings.AUTH_USER_MODEL)
                 ),
            ],
            options={
                'ordering': ('-published',),
            },
        ),
    ]
