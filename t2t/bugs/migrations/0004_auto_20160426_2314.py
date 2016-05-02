# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-26 20:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0003_auto_20160426_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='creator',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reviewers',
            field=models.ManyToManyField(default=None, related_name='reviewers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='watchers',
            field=models.ManyToManyField(default=None, related_name='watchers', to=settings.AUTH_USER_MODEL),
        ),
    ]