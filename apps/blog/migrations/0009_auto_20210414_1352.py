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

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210411_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.TextField(
                blank=True,
                help_text='A short, concise introduction.',
                max_length=256,
                null=True,
                verbose_name='Excerpt',
            ),
        ),
        migrations.AlterField(
            model_name='post',
            name='no_index',
            field=models.BooleanField(
                default=False,
                help_text='Prevent this page from appearing in search index.',
                verbose_name='Block search indexing',
            ),
        ),
        migrations.CreateModel(
            name='Comment',
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
                    'user_name',
                    models.CharField(
                        help_text=('The name of the user '
                                   'who posted the comment.'),
                        max_length=40,
                        verbose_name='User name',
                    )
                ),
                (
                    'user_email',
                    models.EmailField(
                        help_text=('The email of the user who '
                                   'posted the comment.'),
                        max_length=254,
                        verbose_name='E-Mail',
                    )
                ),
                (
                    'comment',
                    models.TextField(
                        help_text='The actual content of the comment itself.',
                        verbose_name='Comment',
                    )
                ),
                (
                    'status',
                    models.CharField(
                        choices=[
                            ('hidden', 'Hidden'),
                            ('published', 'Published'),
                        ],
                        default='hidden',
                        help_text=('Is the comment will be displayed '
                                   'on the site?'),
                        max_length=10,
                        verbose_name='Status',
                    )
                ),
                (
                    'post',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='comments',
                        to='blog.post',
                        verbose_name='Post',
                    )
                ),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('created_at',),
            },
        ),
    ]
