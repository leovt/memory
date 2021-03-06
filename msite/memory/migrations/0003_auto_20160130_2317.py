# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import memory.models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0002_auto_20160130_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='urlid',
            field=models.CharField(default=memory.models._default_urlid, max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='secretid',
            field=models.CharField(default=memory.models._default_secretid, max_length=10, unique=True),
        ),
    ]
