# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-16 16:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mess', '0005_remove_chatmessage_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
