# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Admin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=10)
    admin_password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'admin'

    def __unicode__(self):
        return self.admin_id


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(unique=True, max_length=100)
    discipline = models.ForeignKey('Discipline')
    type_of_course = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.course_name

    class Meta:
        db_table = 'course'


class Discipline(models.Model):
    discipline_id = models.AutoField(primary_key=True)
    discipline = models.CharField(unique=True, max_length=100)

    def __unicode__(self):
        return self.discipline

    class Meta:
        db_table = 'discipline'

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    file_type = models.CharField(max_length=100)
    actual_path = models.FileField(upload_to="files")
    txt_path = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100,unique=True)
    course_id_fk = models.ForeignKey(Course, db_column='course_id_fk')

    def __unicode__(self):
        return self.file_name

    class Meta:
        db_table = 'file'

class Keyword(models.Model):
    file_id_fk = models.ForeignKey(File, db_column='file_id_fk')
    keyword = models.CharField(max_length=100)

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'keyword'
        unique_together = (('file_id_fk', 'keyword'),)

class TempKeyword(models.Model):
    file_id_fk = models.ForeignKey(File, db_column='file_id_fk')
    keyword = models.CharField(max_length=100)

    def __unicode__(self):
        return self.keyword

    class Meta:
        db_table = 'temp_keyword'
        unique_together = (('file_id_fk', 'keyword'),)
