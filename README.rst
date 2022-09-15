=====
Migration Rollback
=====

A Django app used to just make the `python manage.py migrate` a little easier for other Django apps
that commit their migrations and want a way to rollback to a previous migration without needing to
check what the previous migration is via `python manage.py showmigrations` and migrate back to the migration present
in the main git repository for the project.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "migration_rollback" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'migration_rollback',
    ]
