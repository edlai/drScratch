# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0056_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreatorHash',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashkey', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='creator',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterModelManagers(
            name='creator',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='creator',
            name='password',
        ),
        migrations.RemoveField(
            model_name='creator',
            name='username',
        ),
        migrations.AddField(
            model_name='creator',
            name='hashkey',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='challenge',
            name='creator',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='participant',
            name='creator',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='creator',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='creator',
            field=models.CharField(max_length=100),
        ),
        migrations.RemoveField(
            model_name='creator',
            name='id',
        ),
        migrations.AddField(
            model_name='creator',
            name='user_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, default='', serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
