# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20150630_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='time',
        ),
        migrations.AddField(
            model_name='file',
            name='time',
            field=models.DateTimeField(),
            preserve_default=True,
        ), 
    ]
