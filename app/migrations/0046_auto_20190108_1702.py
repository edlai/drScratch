# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20181230_1800'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='img',
        ),
        migrations.AddField(
            model_name='team',
            name='creator',
            field=models.ForeignKey(default=1, to='app.Creator'),
            preserve_default=False,
        ),
    ]
