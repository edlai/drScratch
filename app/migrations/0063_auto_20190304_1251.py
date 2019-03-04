# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('app', '0062_tournament_notificationperiod'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coder',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('birthmonth', models.CharField(max_length=100)),
                ('birthyear', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('gender_other', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('img', models.ImageField(default=b'app/images/drScratch.png', upload_to=b'img/')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='file',
            name='abstraction',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='dataRepresentation',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='deadCode',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='flowControl',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='initialization',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='logic',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='parallelization',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='spriteNaming',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='synchronization',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='file',
            name='userInteractivity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='game',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]
