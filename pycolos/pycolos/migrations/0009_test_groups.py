# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-10 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('pycolos', '0008_question_additional_tests'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
    ]
