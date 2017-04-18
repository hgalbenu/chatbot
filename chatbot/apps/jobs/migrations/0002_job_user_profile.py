# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-18 14:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='user_profile',
            field=models.ForeignKey(help_text='The user profile that this job belongs to.', on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='profiles.UserProfile', verbose_name='user profile'),
        ),
    ]
