# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-19 06:38
from __future__ import unicode_literals

import chatbot.apps.common.model_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motion_ai', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motionai',
            name='reply',
            field=chatbot.apps.common.model_fields.LongCharField(blank=True, max_length=1000000000, null=True, verbose_name='reply'),
        ),
        migrations.AlterField(
            model_name='motionai',
            name='session_id',
            field=chatbot.apps.common.model_fields.LongCharField(blank=True, max_length=1000000000, null=True, verbose_name='session id'),
        ),
    ]
