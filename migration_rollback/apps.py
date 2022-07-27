from django.apps import AppConfig


class MigrationRollbackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'migration_rollback'
