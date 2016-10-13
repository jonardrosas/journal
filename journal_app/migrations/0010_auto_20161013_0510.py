# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0009_auto_20161013_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='journal',
            name='name',
            field=models.CharField(unique=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='journal_entry',
            name='title',
            field=models.CharField(unique=True, max_length=120),
        ),
    ]
