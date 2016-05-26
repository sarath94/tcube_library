# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0003_auto_20160522_0924'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
            ],
        ),
    ]
