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
            help='Migration back to the previous migration on instance',
        )

    def handle(self, *args, **options):
        # TODO clean up and command validation
        app = options['app']
        
        if options['previous-migration']:
            # Ignore what is in git just go back to previous migration
            self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to previous migration"))
            
            previous_migration = get_previous_migration(app=options["app"])

            rollback(app=options["app"], migration=previous_migration)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully rolled back to {previous_migration}"))
        
        branch = options["branch"]
        self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to latest migration on branch {branch}"))
        
        latest_migration_in_git = get_latest_migration_in_git(app=options["app"], branch=options["branch"])
        rollback(app=options["app"], migration=latest_migration_in_git)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully rolled back to {latest_migration_in_git}"))
            
        

            