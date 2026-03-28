from django.core.management.base import BaseCommand, CommandError
from django.core import management

from migration_rollback.utils.migration_utils import (
    get_latest_migration_in_git,
    get_all_migrated_app_names,
)


class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations to match a branch in a git repository."

    def add_arguments(self, parser):
        parser.add_argument("apps", nargs="*", type=str, help="One or more apps to rollback. Omit to rollback all non-system apps.")
        parser.add_argument("--branch", default="main", help="The git branch you wish to rollback to.")
        parser.add_argument(
            "--include-system-apps",
            action="store_true",
            help="Include Django system apps (auth, admin, contenttypes, sessions) when rolling back all apps.",
        )
        parser.add_argument("--fake", action="store_true", help="Mark migrations as run without actually running them.")
        parser.add_argument(
            "--fake-initial", action="store_true", help="Detect if tables already exist and fake-apply initial migrations if so."
        )

    def handle(self, *args, **options):
        apps = options["apps"]
        branch = options["branch"]
        fake = options["fake"]
        fake_initial = options["fake_initial"]
        include_system_apps = options["include_system_apps"]

        if apps:
            for app in apps:
                self._rollback_app(app, branch, fake=fake, fake_initial=fake_initial)
        else:
            app_names = get_all_migrated_app_names(include_system_apps=include_system_apps)
            if not app_names:
                raise CommandError("No apps with applied migrations were found.")
            self.stdout.write(self.style.MIGRATE_HEADING(f"Rolling back all apps to latest migration on branch '{branch}'"))
            for app_name in app_names:
                self._rollback_app(app_name, branch, fake=fake, fake_initial=fake_initial)

    def _rollback_app(self, app: str, branch: str, fake: bool = False, fake_initial: bool = False):
        self.stdout.write(self.style.MIGRATE_HEADING(f"Attempting to rollback {app} to latest migration on branch '{branch}'"))

        if not (latest_migration_in_git := get_latest_migration_in_git(app_name=app, branch_name=branch)):
            raise CommandError(f"Unable to rollback {app} to latest migration on branch '{branch}' since no migration was found.")

        management.call_command(
            "migrate",
            app,
            latest_migration_in_git,
            fake=fake,
            fake_initial=fake_initial,
            stdout=self.stdout,
            stderr=self.stderr,
        )
