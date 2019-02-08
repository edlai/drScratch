# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0058_auto_20190207_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='participant',
        ),
        migrations.AddField(
            model_name='participant',
            name='teams',
            field=models.ManyToManyField(to='app.Team'),
        ),
    ]
