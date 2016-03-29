# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_current_participants_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participant',
            old_name='event_id',
            new_name='event',
        ),
        migrations.RenameField(
            model_name='participant',
            old_name='user_id',
            new_name='user',
        ),
    ]
