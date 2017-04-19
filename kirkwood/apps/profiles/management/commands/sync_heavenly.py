import time

from django.core.management.base import BaseCommand

from ...models import UserProfile


class Command(BaseCommand):
    help = 'Syncs all user profiles to heavenly'

    def handle(self, *args, **options):
        user_profiles = UserProfile.objects.prefetch_related('jobs', 'debts')
        for profile in user_profiles:
            print(user_profiles.email)
            # clear heavenly data first, this way the before_update listener kicks in and does a heavenly sync
            profile.heavenly_request = None
            profile.heavenly_response = None
            profile.heavenly_updated_at = None
            profile.save()
            time.sleep(1)
