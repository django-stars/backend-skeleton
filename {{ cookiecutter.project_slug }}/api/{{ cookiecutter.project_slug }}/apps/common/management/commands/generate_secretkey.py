from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Generates a secret key."
    requires_system_checks = []

    def handle(self, *args, **options):
        secret_key = get_random_secret_key()
        self.stdout.write(self.style.SUCCESS(secret_key))
