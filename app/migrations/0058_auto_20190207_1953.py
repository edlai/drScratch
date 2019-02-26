# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0057_auto_20190206_1837'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='participant',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='participant',
            name='email',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='password',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='username',
        ),
        migrations.AddField(
            model_name='tournament',
            name='manualValidation',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='game',
            name='completed',
        ),
        migrations.AddField(
            model_name='game',
            name='completed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='team',
            name='participant',
        ),
        migrations.AddField(
            model_name='team',
            name='participant',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='participant',
            name='id',
        ),
        migrations.AddField(
            model_name='participant',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='', serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
