from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name='user', related_name='user_profile')

    def __unicode__(self):
        return str(self.user) + "'s profile."
