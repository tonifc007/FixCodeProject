# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 16:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='participations',
            name='ativa_notificacao',
            field=models.BooleanField(default=True),
        ),
    ]
