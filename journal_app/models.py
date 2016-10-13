from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Journal(models.Model):
    TYPE_CHOICES = (
        ("personal", "Personal"),
        ("academic", "Academic"),
    )

    name = models.CharField(max_length=120)
    description = models.CharField(
        max_length=12,
        choices=TYPE_CHOICES,
        default="personal")
    created_by = models.ForeignKey(User, related_name='+')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return (self.name)


class Journal_entry(models.Model):
    journal_id = models.ForeignKey(
        Journal,
        related_name="journal_entry",
        null=True,
        blank=True, default=None
    )
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return (self.title)
