# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-27 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_comentpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='exibir_perfil',
            field=models.BooleanField(default=True),
        ),
    ]
