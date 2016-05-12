# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_ortoloco', '0003_auto_20160119_1113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractjobtype',
            name='bereich',
        ),
        migrations.RemoveField(
            model_name='abstractjobtype',
            name='polymorphic_ctype',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='bereicht',
            new_name='bereich',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='descriptiont',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='displayed_namet',
            new_name='displayed_name',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='durationt',
            new_name='duration',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='locationt',
            new_name='location',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='bereichp',
            new_name='bereich',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='descriptionp',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='displayed_namep',
            new_name='displayed_name',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='durationp',
            new_name='duration',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='locationp',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='jobtype',
            name='abstractjobtype_ptr',
        ),
        migrations.RenameField(
            model_name='jobtype',
            old_name='namet',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='onetimejob',
            name='abstractjobtype_ptr',
        ),
        migrations.RenameField(
            model_name='onetimejob',
            old_name='namep',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='jobtype',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name=b'Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='onetimejob',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True, verbose_name=b'Name'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='AbstractJobType',
        ),
    ]
