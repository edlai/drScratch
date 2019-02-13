# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0061_game_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='notificationPeriod',
            field=models.IntegerField(default=0),
        ),
    ]
