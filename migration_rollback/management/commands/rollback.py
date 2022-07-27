from django.core.management.base import BaseCommand, CommandError

import subprocess

class Command(BaseCommand):
    help = "A way to rollback a Django app's migrations"

    def add_arguments(self, parser):
        parser.add_argument("-a","--app", required=True, type=str)
        
        parser.add_argument(
            '--previous-migration',
            action='store_true',
            help='Migration back to the previous migration',
        )

    def handle(self, *args, **options):
        app = options['app']
        
        if options['previous-migration']:
            self.stdout.write(self.style.SUCCESS(f"Attempting to go back to roll back {app} to previous migration"))