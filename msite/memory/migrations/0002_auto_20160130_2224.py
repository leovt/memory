# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-30 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='memory.Player'),
        ),
    ]
