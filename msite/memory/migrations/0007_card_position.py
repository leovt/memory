# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 20:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0006_auto_20160204_2041'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='position',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
