# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0010_auto_20161013_0510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='name',
            field=models.CharField(max_length=120),
        ),
    ]
