from django.core.management.base import BaseCommand, CommandError

from migration_rollback.utils.migration_utils import get_latest_migration_in_git, get_previous_migration, rollback

class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations"

    def add_arguments(self, parser):
        parser.add_argument("-a","--app", required=True, type=str)
        parser.add_argument("-b", "--branch", required=False, type=str)
        
        parser.add_argument(
            '--previous-migration',
            action='store_true',
            default=True,
            required=False,
            help='Migration back to the previous migration on instance',
        )

    def handle(self, *args, **options):
        app = options['app']
        branch = options["branch"]
        
        self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to latest migration on branch {branch}"))
        
        latest_migration_in_git = get_latest_migration_in_git(app_name=app, branch_name=branch)
        rollback(app_name=app, migration=latest_migration_in_git)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully rolled back to {latest_migration_in_git}"))
            
        

            