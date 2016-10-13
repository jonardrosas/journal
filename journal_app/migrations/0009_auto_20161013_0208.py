# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0008_auto_20161001_1430'),
    ]

    operations = [
        migrations.RenameField(
            model_name='journal',
            old_name='type',
            new_name='description',
        ),
    ]
