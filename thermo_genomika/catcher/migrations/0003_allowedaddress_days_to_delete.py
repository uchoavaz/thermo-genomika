# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-24 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catcher', '0002_allowedaddress_max_temperature'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowedaddress',
            name='days_to_delete',
            field=models.IntegerField(default=30, verbose_name='Days to delete'),
        ),
    ]