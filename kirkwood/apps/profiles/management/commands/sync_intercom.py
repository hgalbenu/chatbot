import time

from django.core.management.base import BaseCommand

from ...models import UserProfile


class Command(BaseCommand):
    help = 'Syncs all user profiles to intercom'

    def handle(self, *args, **options):
        user_profiles = UserProfile.objects.all()
        for profile in user_profiles:
            print(user_profiles.email)
            profile.to_intercom()
            profile.save()
            time.sleep(1)
