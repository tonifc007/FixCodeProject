# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20161016_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='habilidades',
            field=models.ManyToManyField(max_length=5, to='core.Areas'),
        ),
    ]