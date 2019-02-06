# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0049_auto_20190110_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parallelism', models.IntegerField(default=0)),
                ('logic', models.IntegerField(default=0)),
                ('flowControl', models.IntegerField(default=0)),
                ('userInteractivity', models.IntegerField(default=0)),
                ('dataRepresentation', models.IntegerField(default=0)),
                ('abstraction', models.IntegerField(default=0)),
                ('synchronization', models.IntegerField(default=0)),
                ('challenge', models.ForeignKey(to='app.Challenge')),
                ('participant', models.ForeignKey(to='app.Participant')),
            ],
        ),
    ]
