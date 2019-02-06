# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20190108_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='img',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='team',
            name='num_participants',
        ),
        migrations.RemoveField(
            model_name='team',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='img',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='num_teams',
        ),
        migrations.AddField(
            model_name='participant',
            name='email',
            field=models.CharField(unique=True, max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='team',
            name='participant',
            field=models.ManyToManyField(to='app.Participant'),
        ),
        migrations.AddField(
            model_name='team',
            name='tournaments',
            field=models.ManyToManyField(to='app.Tournament'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='username',
            field=models.TextField(),
        ),
    ]
