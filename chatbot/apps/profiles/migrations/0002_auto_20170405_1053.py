# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-05 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='total_debt',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=25, null=True, verbose_name='total debt'),
        ),
    ]
