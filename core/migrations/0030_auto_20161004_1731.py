# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 20:31
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20161003_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentpost',
            name='coment',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
