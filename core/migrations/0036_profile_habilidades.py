# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20161015_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='habilidades',
            field=models.ManyToManyField(to='core.Areas'),
        ),
    ]
