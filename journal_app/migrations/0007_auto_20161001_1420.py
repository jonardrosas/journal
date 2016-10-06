# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0006_auto_20161001_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='type',
            field=models.CharField(default='Personal', max_length=20, choices=[('personal', 'Personal'), ('academic', 'Academic')]),
        ),
    ]
