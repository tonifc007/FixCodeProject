# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-04 21:55
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_auto_20161004_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentfixies',
            name='coment',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='fixies',
            name='descricao',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
