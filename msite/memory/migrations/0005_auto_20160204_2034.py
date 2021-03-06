# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-04 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0004_card_shown'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='memory.Player'),
        ),
        migrations.AlterField(
            model_name='game',
            name='status',
            field=models.IntegerField(choices=[(0, 'wait for players'), (1, 'no card shown'), (2, 'one card shown'), (3, 'two different cards shown'), (4, 'two identical cards shown'), (5, 'game ended')], default=0),
        ),
    ]
