# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 08:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20170525_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 25, 8, 9, 35, 92406, tzinfo=utc)),
        ),
    ]
