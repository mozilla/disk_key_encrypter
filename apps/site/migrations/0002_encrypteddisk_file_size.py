# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-05-01 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='encrypteddisk',
            name='file_size',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]