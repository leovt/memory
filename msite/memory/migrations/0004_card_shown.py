# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-01 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0003_auto_20160130_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='shown',
            field=models.BooleanField(default=False),
        ),
    ]