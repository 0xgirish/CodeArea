# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-01 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0005_auto_20180428_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
