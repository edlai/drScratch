# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-01-21 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20170121_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='img',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='participant',
            name='name',
            field=models.TextField(default=b''),
        ),
    ]
