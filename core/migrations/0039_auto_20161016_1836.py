# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20161016_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='habilidades',
            field=models.ManyToManyField(to='core.Areas'),
        ),
    ]
