# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-28 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0005_auto_20180425_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
