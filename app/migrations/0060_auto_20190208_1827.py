# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0059_auto_20190207_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='creator',
            new_name='creator_username',
        ),
    ]
