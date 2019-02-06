# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20190121_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challengesoftournament',
            name='challenge',
            field=models.ForeignKey(related_name='chall', to='app.Challenge'),
        ),
    ]
