# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='event_id',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
