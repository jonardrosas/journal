# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0005_journal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='type',
            field=models.IntegerField(default=1, choices=[(1, 'Personal'), (2, 'Academic')]),
        ),
    ]
