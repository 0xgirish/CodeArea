# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-06 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_auto_20180305_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]