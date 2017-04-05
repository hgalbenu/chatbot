from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name='user', related_name='user_profile')

    date_of_birth = models.DateField(verbose_name='date of birth', blank=True, null=True)
    total_debt = models.DecimalField(decimal_places=2, max_digits=25, verbose_name='total debt', blank=True, null=True)

    @property
    def full_name(self):
        return self.user.get_full_name()

    @full_name.setter
    def full_name(self, value):
        user = self.user
        first_name, last_name = value.split(' ')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    @property
    def email(self):
        return self.user.email

    @email.setter
    def email(self, value):
        user = self.user
        user.email = value
        user.save()

    def __unicode__(self):
        return str(self.user) + "'s profile."
