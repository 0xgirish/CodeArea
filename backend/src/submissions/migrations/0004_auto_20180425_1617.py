# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-25 16:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_problem_level'),
        ('submissions', '0003_auto_20180307_0953'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmissionTasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('AC', 'ACCEPTED'), ('WA', 'WRONG ANSWER'), ('RE', 'RUNTIME ERROR'), ('TLE', 'TIME LIMIT EXCEEDED'), ('IE', 'INTERNAL ERROR'), ('R', 'RUNNING')], default='R', max_length=3)),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='submissions.Submission')),
                ('testcase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.TestCase')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='testcases',
            field=models.ManyToManyField(through='submissions.SubmissionTasks', to='problems.TestCase'),
        ),
    ]