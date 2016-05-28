# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0005_delete_textsearch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_name',
            field=models.CharField(unique=True, max_length=45),
        ),
    ]
