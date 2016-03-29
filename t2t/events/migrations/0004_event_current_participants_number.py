# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20160320_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='current_participants_number',
            field=models.IntegerField(default=0),
        ),
    ]
