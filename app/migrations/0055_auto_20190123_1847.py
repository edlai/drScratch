# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20190122_1936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='challenge',
        ),
        migrations.AddField(
            model_name='game',
            name='challengeOfTournament',
            field=models.ForeignKey(default=5, to='app.ChallengesOfTournament'),
            preserve_default=False,
        ),
    ]
