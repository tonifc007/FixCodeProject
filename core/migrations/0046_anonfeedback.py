# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-27 08:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_profile_ativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('texto', models.TextField(verbose_name='Texto')),
            ],
        ),
    ]