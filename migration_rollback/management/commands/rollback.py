from django.core.management.base import BaseCommand, CommandError

from migration_rollback.utils.migration_utils import get_latest_migration_in_git, get_previous_migration, rollback

class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations"

    def add_arguments(self, parser):
        parser.add_argument("-a","--app", required=True, type=str)
        parser.add_argument("-b", "--branch", required=False, type=str, default="main")

    def handle(self, *args, **options):
        # TODO clean up and command validation
        app = options['app']
        
        branch = options["branch"]
        self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to latest migration on branch {branch}"))
        
        latest_migration_in_git = get_latest_migration_in_git(app=app, branch=branch)
        rollback(app=app, migration=latest_migration_in_git)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully rolled back to {latest_migration_in_git}"))
            
        

            