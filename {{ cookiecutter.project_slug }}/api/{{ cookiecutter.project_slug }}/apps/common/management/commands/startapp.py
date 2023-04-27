import os

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as StartappCommand


class Command(StartappCommand):
    def handle(self, **options):
        if options["directory"] is None:
            app_directory = os.path.join(settings.BASE_DIR, "apps", options["name"])

            try:
                os.makedirs(app_directory, exist_ok=True)
            except FileExistsError:
                raise CommandError(f"'{app_directory}' already exists")  # pylint: disable=raise-missing-from

            options["directory"] = app_directory

        super().handle(**options)
