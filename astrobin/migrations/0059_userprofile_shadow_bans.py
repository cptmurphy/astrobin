# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-07 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrobin', '0058_sort_remote_sources'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='shadow_bans',
            field=models.ManyToManyField(to='astrobin.UserProfile'),
        ),
    ]