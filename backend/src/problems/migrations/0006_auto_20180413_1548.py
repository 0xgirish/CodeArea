# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-13 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_testcase_explanation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, to='tags.Tag'),
        ),
    ]
