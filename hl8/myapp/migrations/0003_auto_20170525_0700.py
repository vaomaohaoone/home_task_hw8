# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-25 07:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20170525_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 25, 7, 0, 28, 587027, tzinfo=utc)),
        ),
    ]
