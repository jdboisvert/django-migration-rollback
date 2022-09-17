from django.core.management.base import BaseCommand, CommandError
from django.core import management

from migration_rollback.utils.migration_utils import (
    get_latest_migration_in_git,
)


class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations to match a branch in a git repository."

    def add_arguments(self, parser):
        parser.add_argument("app", nargs="?", type=str, help="The app you wish to run the migrations against")
        parser.add_argument("branch", nargs="?", type=str, default="main", help="The git branch you wish to rollback to.")

    def handle(self, *args, **options):
        app = options["app"]
        branch = options["branch"]

        self.stdout.write(self.style.MIGRATE_HEADING(f"Attempting to go back to rollback {app} to latest migration on branch {branch}"))

        if branch:
            if not (latest_migration_in_git := get_latest_migration_in_git(app_name=app, branch_name=branch)):
                raise CommandError(f"Unable to rollback {app} to latest migration on branch {branch} since no migration was found.")

            management.call_command(
                "migrate",
                app,
                latest_migration_in_git,
                stdout=self.stdout,
                stderr=self.stderr,
            )
