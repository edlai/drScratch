# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0050_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
