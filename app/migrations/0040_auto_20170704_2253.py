# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-07-04 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20170704_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='name',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]