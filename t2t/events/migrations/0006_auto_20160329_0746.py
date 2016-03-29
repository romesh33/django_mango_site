# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0005_auto_20160326_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='event',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='user',
        ),
        migrations.AddField(
            model_name='event',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
