# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 06:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creditors', '0002_auto_20170418_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditor',
            name='total_debt',
        ),
    ]
