# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0011_auto_20161014_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal_entry',
            name='title',
            field=models.CharField(max_length=120),
        ),
    ]
