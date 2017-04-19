from django.core.management.base import BaseCommand
from django.db import connection

from ...sql_views import USER_WITH_EXTERNAL_LINKS_QUERY


class Command(BaseCommand):
    help = 'Drops and recreates db views'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP VIEW IF EXISTS user_with_external_links")
            cursor.execute(USER_WITH_EXTERNAL_LINKS_QUERY)

        self.stdout.write('All db views are up to date.')
