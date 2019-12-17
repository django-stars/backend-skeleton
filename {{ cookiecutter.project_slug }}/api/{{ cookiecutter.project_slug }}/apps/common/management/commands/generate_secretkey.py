import string

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("length", type=int)

    def handle(self, *args, **options):
        print(
            get_random_string(
                length=options["length"], allowed_chars=string.ascii_letters + string.digits + string.punctuation
            )
        )
