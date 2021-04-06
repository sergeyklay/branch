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
        ('blog', '0002_post_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.TextField(
                blank=True,
                help_text='A short, concise introduction',
                max_length=256,
                null=True,
                verbose_name='excerpt',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.TextField(
                blank=True,
                default='',
                help_text=('This will be displayed in meta tags. '
                           'Keep it under 120 characters.'),
                max_length=256,
                verbose_name='Meta description',
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='meta_title',
            field=models.CharField(
                blank=True,
                default='',
                help_text=('This will be displayed in meta tags. '
                           'Keep it under 60 characters. '
                           "Leave empty and the post's title will be used."),
                max_length=60,
                verbose_name='Meta title',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(
                verbose_name='Full text of the post',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(
                auto_now_add=True,
                verbose_name='Date created',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name='First publication date',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(
                help_text='Let it empty so it will be autopopulated.',
                max_length=250,
                unique_for_date='published_at',
                verbose_name='Slug',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(
                auto_now=True,
                verbose_name='Date updated',
            ),
        ),
    ]
