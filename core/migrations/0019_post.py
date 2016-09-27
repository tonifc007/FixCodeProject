# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-26 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0018_fixies_ativa_notificacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('post', models.TextField()),
                ('data', models.DateTimeField(default=django.utils.timezone.now)),
                ('notificacao', models.IntegerField(default=0)),
                ('ativa_notificacao', models.BooleanField(default=True)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
