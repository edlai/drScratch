# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_participant_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='teams',
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='tournament',
        ),
        migrations.AddField(
            model_name='challenge',
            name='creator',
            field=models.ForeignKey(default=1, to='app.Creator'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challenge',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='challenge',
            name='tournaments',
            field=models.ManyToManyField(to='app.Tournament'),
        ),
    ]
