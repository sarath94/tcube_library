# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempKeyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=45)),
                ('file_id_fk', models.ForeignKey(to='work.File', db_column='file_id_fk')),
            ],
            options={
                'db_table': 'temp_keyword',
            },
        ),
        migrations.AlterUniqueTogether(
            name='tempkeyword',
            unique_together=set([('file_id_fk', 'keyword')]),
        ),
    ]
