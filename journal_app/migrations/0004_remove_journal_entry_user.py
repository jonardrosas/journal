# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal_app', '0003_journal_journal_entry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journal_entry',
            name='user',
        ),
    ]
