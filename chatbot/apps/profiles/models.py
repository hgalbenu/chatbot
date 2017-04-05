from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'), related_name='user_profile')

    def __unicode__(self):
        return str(self.user) + _("'s profile.")