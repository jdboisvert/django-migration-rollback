from django.core.management.base import BaseCommand, CommandError

from django.core import management

from migration_rollback.utils.migration_utils import (
    get_previous_migration,
    get_all_migrated_app_names,
)


class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations to the previous migration."

    def add_arguments(self, parser):
        parser.add_argument(
            "app", nargs="?", type=str, help="The app you wish to run the migrations against. Omit to rollback all non-system apps."
        )
        parser.add_argument(
            "--include-system-apps",
            action="store_true",
            help=(
                "Include Django system apps (auth, admin, contenttypes, sessions) when rolling back all apps. "
                "WARNING: system apps have cross-app dependencies that can cause unexpected cascading rollbacks. "
                "Use with caution."
            ),
        )
        parser.add_argument(
            "--yes",
            "-y",
            action="store_true",
            help="Skip the confirmation prompt when rolling back all apps. Useful for CI environments.",
        )
        parser.add_argument("--fake", action="store_true", help="Mark migrations as run without actually running them.")
        parser.add_argument(
            "--fake-initial", action="store_true", help="Detect if tables already exist and fake-apply initial migrations if so."
        )

    def handle(self, *args, **options):
        app = options["app"]
        fake = options["fake"]
        fake_initial = options["fake_initial"]
        include_system_apps = options["include_system_apps"]
        yes = options["yes"]

        if app:
            self._rollback_app(app, fake=fake, fake_initial=fake_initial)
        else:
            app_names = get_all_migrated_app_names(include_system_apps=include_system_apps)
            if not app_names:
                raise CommandError("No apps with applied migrations were found.")

            self.stdout.write(self.style.MIGRATE_HEADING("The following apps will be rolled back to their previous migration:"))
            for app_name in app_names:
                self.stdout.write(f"  - {app_name}")

            if not yes:
                confirm = input("\nAre you sure you want to continue? [y/N] ").strip().lower()
                if confirm != "y":
                    raise CommandError("Rollback cancelled.")

            self.stdout.write(self.style.MIGRATE_HEADING("Rolling back all apps to their previous migration"))
            for app_name in app_names:
                self._rollback_app(app_name, fake=fake, fake_initial=fake_initial)

    def _rollback_app(self, app: str, fake: bool = False, fake_initial: bool = False):
        self.stdout.write(self.style.MIGRATE_HEADING(f"Attempting to rollback {app} to previous migration"))

        if not (previous_migration := get_previous_migration(app_name=app)):
            raise CommandError(f"Unable to rollback {app} to previous migration since no migration was found.")

        management.call_command(
            "migrate",
            app,
            previous_migration,
            fake=fake,
            fake_initial=fake_initial,
            stdout=self.stdout,
            stderr=self.stderr,
        )
