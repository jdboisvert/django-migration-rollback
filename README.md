# Django Migration Rollback
A Django package used to just make the `python manage.py migrate` a little easier for Django apps that commit their migrations and want a way to rollback to a previous migration without needing to check what the which one it is via `python manage.py showmigrations` or in the project's git repository.

## Features
Able to set which branch in a git repository to rollback to using the custom command `migraterollback` or if you wish to just rollback to a previous migration only via `migrateprevious`. Note in order to use the rollback with a git repository's branch feature with git the project must have a `.git` file present.

### Django migraterollback command
    ❯ python manage.py migraterollback polls feature/really-cool-branch

This command is used to migrate a Django app back to the migration found in a repository's branch (this will also migrate to that migration if behind).

* An app must be specified as the first argument after the command to indicate which app you wish to rollback.
* By default if no argument is specified after the app, the branch `main` will be used.

### Django migrateprevious
    ❯ python manage.py migrateprevious polls

This command is used to migrate a Django app back to the previously applied migration.

* An app must be specified as the first argument after the command to indicate which app you wish to migrate to the previously applied migration.

## Installing
### From PyPi
    ❯ pip install django-migration-rollback

### From GitHub
    ❯ pip install git+ssh://git@github.com/jdboisvert/django-migration-rollback


### Quick start
Add "migration_rollback" to your INSTALLED_APPS in the `settings.py` like this:
```
    INSTALLED_APPS = [
        ...
        'migration_rollback',
    ]
```
