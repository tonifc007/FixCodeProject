# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 01:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_comentfixies'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentfixies',
            name='melhor_resposta',
            field=models.BooleanField(default=False),
        ),
    ]
