# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-15 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20161004_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='habilidades',
            field=models.CharField(choices=[('c', 'C'), ('python', 'Python')], default=False, max_length=2),
        ),
    ]
