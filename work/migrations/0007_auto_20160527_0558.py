# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_auto_20160526_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='admin_password',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='course',
            name='type_of_course',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='discipline',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='file_type',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='file',
            name='txt_path',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='keyword',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tempkeyword',
            name='keyword',
            field=models.CharField(max_length=100),
        ),
    ]
