# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0051_game_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='participant',
        ),
        migrations.AddField(
            model_name='game',
            name='team',
            field=models.ForeignKey(default=3, to='app.Team'),
            preserve_default=False,
        ),
    ]
