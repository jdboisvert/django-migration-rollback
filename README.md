# django-migration-rollback
A Django package used to just make the `python manage.py migrate` a little easier for Django applications that commit their migrations and want a way to rollback to a previous migration without needing to check what the previous migration is via `python manage.py showmigrations` and migrate back to the migration present in the main git repository for the project. 