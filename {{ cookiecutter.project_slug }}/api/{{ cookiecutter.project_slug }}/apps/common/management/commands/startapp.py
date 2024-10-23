from pathlib import Path

from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.startapp import Command as StartappCommand


class Command(StartappCommand):
    def handle(self, **options) -> None:  # noqa: ANN003
        if options["directory"] is None:
            app_directory = Path(settings.BASE_DIR) / "apps" / options["name"]

            try:
                Path(app_directory).mkdir(parents=True, exist_ok=True)
            except FileExistsError as exc:
                message = f"'{app_directory}' already exists"
                raise CommandError(message) from exc

            options["directory"] = app_directory

        super().handle(**options)
