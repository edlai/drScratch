# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20150527_1115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='duplicatedScript',
        ),
        migrations.AddField(
            model_name='file',
            name='duplicateScript',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='file',
            name='abstraction',
        ),
        migrations.AddField(
            model_name='file',
            name='abstraction',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='dataRepresentation',
        ),
        migrations.AddField(
            model_name='file',
            name='dataRepresentation',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='deadCode',
        ),
        migrations.AddField(
            model_name='file',
            name='deadCode',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='flowControl',
        ),
        migrations.AddField(
            model_name='file',
            name='flowControl',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='initialization',
        ),
        migrations.AddField(
            model_name='file',
            name='initialization',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='logic',
        ),
        migrations.AddField(
            model_name='file',
            name='logic',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='parallelization',
        ),
        migrations.AddField(
            model_name='file',
            name='parallelization',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='spriteNaming',
        ),
        migrations.AddField(
            model_name='file',
            name='spriteNaming',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='synchronization',
        ),
        migrations.AddField(
            model_name='file',
            name='synchronization',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='file',
            name='userInteractivity',
        ),
        migrations.AddField(
            model_name='file',
            name='userInteractivity',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
