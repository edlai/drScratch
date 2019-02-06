# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0052_auto_20190117_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChallengesOfTournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.RemoveField(
            model_name='challenge',
            name='tournaments',
        ),
        migrations.RemoveField(
            model_name='team',
            name='tournaments',
        ),
        migrations.AddField(
            model_name='tournament',
            name='teams',
            field=models.ManyToManyField(to='app.Team'),
        ),
        migrations.AddField(
            model_name='challengesoftournament',
            name='challenge',
            field=models.ForeignKey(to='app.Challenge'),
        ),
        migrations.AddField(
            model_name='challengesoftournament',
            name='tournament',
            field=models.ForeignKey(to='app.Tournament'),
        ),
        migrations.AddField(
            model_name='tournament',
            name='challenges',
            field=models.ManyToManyField(to='app.Challenge', through='app.ChallengesOfTournament'),
        ),
    ]
