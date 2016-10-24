from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Journal(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    created_by = models.ForeignKey(User, related_name='created_by')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return (self.name)

    def created_by_field(self):
       return self.created_by
    created_by_field.short_description = 'Created by'

    def date_created_field(self):
       return self.date_created
    date_created_field.short_description = 'Date created'




class Journal_entry(models.Model):
    journal_id = models.ForeignKey(
        Journal,
        related_name="journal_entry",
        null=False,
        blank=False, default=None
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return (self.title)

    def entry_date_created(self):
       return self.date_created
    entry_date_created.short_description = 'Date created'
