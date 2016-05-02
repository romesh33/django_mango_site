# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-25 06:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0006_auto_20160329_0746'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Саммари по умолчанию', max_length=200)),
                ('description', models.TextField(default='Описание', max_length=2000)),
                ('creation_time', models.DateTimeField(verbose_name='creation time')),
                ('is_bug', models.BooleanField(verbose_name='is_bug')),
                ('is_report', models.BooleanField(verbose_name='is_report')),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='creator_user', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('reviewers', models.ManyToManyField(related_name='reviewers_users', to=settings.AUTH_USER_MODEL)),
                ('watchers', models.ManyToManyField(related_name='watchers_users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
