import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seed database"

    def handle(self, *args, **options):
        logger.debug('-- Seed database -- start:')

        return
