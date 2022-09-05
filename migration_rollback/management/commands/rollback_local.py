from django.core.management.base import BaseCommand, CommandError

from migration_rollback.utils.migration_utils import get_latest_migration_in_git, get_previous_migration, rollback

class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations"

    def add_arguments(self, parser):
        parser.add_argument("-a","--app", required=True, type=str)

    def handle(self, *args, **options):
        app = options['app']
        
        self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to previous migration"))
        
        if not (previous_migration := get_previous_migration(app_name=app)):
            self.stdout.write(self.style.ERROR(f"Unable to rollback {app} to previous migration since no migration was found."))
            return

        rollback(app_name=app, migration=previous_migration)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully rolled back to {previous_migration}"))
            
        

            