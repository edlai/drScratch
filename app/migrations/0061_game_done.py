# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_auto_20190208_1827'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='done',
            field=models.IntegerField(default=0),
        ),
    ]
