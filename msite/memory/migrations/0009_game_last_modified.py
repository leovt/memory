# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 19:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0008_auto_20160205_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]
