from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    text_password = models.CharField(max_length=500, null=True)
