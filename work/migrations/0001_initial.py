# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('admin_id', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('admin_password', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_id', models.AutoField(serialize=False, primary_key=True)),
                ('course_name', models.CharField(max_length=45)),
                ('type_of_course', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'course',
            },
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('discipline_id', models.AutoField(serialize=False, primary_key=True)),
                ('discipline', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'discipline',
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('file_id', models.AutoField(serialize=False, primary_key=True)),
                ('file_type', models.CharField(max_length=45)),
                ('actual_path', models.FileField(upload_to='files')),
                ('txt_path', models.CharField(max_length=45)),
                ('file_name', models.CharField(max_length=45)),
                ('course_id_fk', models.ForeignKey(to='work.Course', db_column='course_id_fk')),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('keyword', models.CharField(max_length=45)),
                ('file_id_fk', models.ForeignKey(to='work.File', db_column='file_id_fk')),
            ],
            options={
                'db_table': 'keyword',
            },
        ),
        migrations.AddField(
            model_name='course',
            name='discipline',
            field=models.ForeignKey(to='work.Discipline'),
        ),
        migrations.AlterUniqueTogether(
            name='keyword',
            unique_together=set([('file_id_fk', 'keyword')]),
        ),
    ]
