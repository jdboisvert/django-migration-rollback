# Django Migration Rollback
A Django package used to just make the `python manage.py migrate` a little easier for Django apps that commit their migrations and want a way to rollback to a previous migration without needing to check what the which one it is via `python manage.py showmigrations` or in the project's git repository.

## Features
Able to set which branch in a git repository to rollback to using the custom command `rollback` or if you wish to just rollback to a previous migration on your local machine via `rollback_local`. Note in order to use the rollback feature with git the project must have a `.git` file present.

### Django rollback command
    ❯ python manage.py rollback -a polls -b feature/really-cool-branch

* By default if no argument is specified for the branch `main` will be used. The argument is specified via `-b`.
* An app must be specified via the `-a` to indicate which app you wish to rollback.

### Django rollback_local
    ❯ python manage.py rollback_local -a polls

* An app must be specified via the `-a` to indicate which app you wish to rollback.
* This will simply migrate back to the previous migration.

## Installing
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
