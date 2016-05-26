# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0002_auto_20160521_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(unique=True, max_length=45),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='discipline',
            field=models.CharField(unique=True, max_length=45),
        ),
    ]
