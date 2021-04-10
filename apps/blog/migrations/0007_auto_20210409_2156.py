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

    dependencies = [
        ('blog', '0006_alter_post_no_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='locale',
            field=models.CharField(
                choices=[
                    ('en_US', 'English'),
                    ('ru_RU', 'Russian'),
                    ('uk_UA', 'Ukrainian'),
                ],
                default='en_US',
                help_text='The locale of the resource.',
                max_length=5,
                verbose_name='Locale'
            ),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(
                choices=[
                    ('drama', 'Drama'),
                    ('narrative', 'Narrative'),
                    ('poem poetry', 'Poem'),
                    ('post', 'Post'),
                ],
                default='post',
                max_length=12,
                verbose_name='Resource type',
            ),
        ),
    ]
