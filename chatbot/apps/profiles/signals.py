import sys

from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver


# Kind of hacky but should do for now, we don't really want to update intercom and heavenly when testing.
if 'test' not in sys.argv:
    @receiver(pre_save)
    def to_heavenly(sender, instance, **kwargs):
        from .models import UserProfile

        if sender == UserProfile:
            instance.to_heavenly()


    @receiver(post_save)
    def to_intercom(sender, instance, **kwargs):
        from .models import UserProfile

        if sender == UserProfile:
            instance.to_intercom()


    @receiver(pre_delete)
    def delete_intercom(sender, instance, **kwargs):
        from .models import UserProfile

        if sender == UserProfile:
            instance.delete_intercom()
