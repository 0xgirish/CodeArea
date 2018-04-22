# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-07 09:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0001_initial'),
        ('accounts', '0001_initial'),
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContestSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('status', models.CharField(choices=[('AC', 'ACCEPTED'), ('WA', 'WRONG ANSWER'), ('RE', 'RUNTIME ERROR'), ('TLE', 'TIME LIMIT EXCEEDED'), ('IE', 'INTERNAL ERROR'), ('R', 'RUNNING')], default='R', max_length=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField()),
                ('status', models.CharField(choices=[('AC', 'ACCEPTED'), ('WA', 'WRONG ANSWER'), ('RE', 'RUNTIME ERROR'), ('TLE', 'TIME LIMIT EXCEEDED'), ('IE', 'INTERNAL ERROR'), ('R', 'RUNNING')], default='R', max_length=3)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.Language')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='problems.Problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='submissions.Language'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.ContestsHaveProblems'),
        ),
        migrations.AddField(
            model_name='contestsubmission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile'),
        ),
    ]