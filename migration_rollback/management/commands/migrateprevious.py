from django.core.management.base import BaseCommand, CommandError

from django.core import management

from migration_rollback.utils.migration_utils import (
    get_previous_migration,
)


class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations to the previous migration."

    def add_arguments(self, parser):
        parser.add_argument("app", nargs="?", type=str, help="The app you wish to run the migrations against")

    def handle(self, *args, **options):
        app = options["app"]

        self.stdout.write(self.style.MIGRATE_HEADING(f"Attempting to go back to rollback {app} to previous migration"))

        if not (previous_migration := get_previous_migration(app_name=app)):
            raise CommandError(f"Unable to rollback {app} to previous migration since no migration was found.")

        management.call_command(
            "migrate",
            app,
            previous_migration,
            stdout=self.stdout,
            stderr=self.stderr,
        )
