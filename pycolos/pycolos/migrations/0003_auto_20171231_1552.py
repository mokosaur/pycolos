# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-31 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pycolos', '0002_auto_20171231_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='available_for_x_minutes',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='available_from',
            field=models.DateTimeField(null=True),
        ),
    ]
