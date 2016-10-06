# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0004_remove_journal_entry_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='type',
            field=models.CharField(default=None, max_length=120),
            preserve_default=False,
        ),
    ]
