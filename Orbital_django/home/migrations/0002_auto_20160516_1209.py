# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_member',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]