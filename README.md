# django-migration-rollback
A Django package used to just make the `python manage.py migrate` a little easier for Django applications that commit their migrations and want a way to rollback to a previous migration without needing to check what the previous migration is via `python manage.py showmigrations` and migrate back to the migration present in the main git repository for the project. 

# Django Migration Rollback v2022.7.26.1
A Django package used to just make the `python manage.py migrate` a little easier for Django applications that commit their migrations and want a way to rollback to a previous migration without needing to check what the previous migration is via `python manage.py showmigrations` and migrate back to the migration present in the main git repository for the project. 

## Features
Able to set which branch in a git repository to rollback to using the custom command `rollback` or if you wish to just rollback to a previous migration via `rollback_local`. Note in order to use the rollback feature with git the project must have a `.git` file present. 

### rollback command
    ❯ python manage.py rollback -a polls -b feature/really-cool-feature

* By default if no argument is specified for the branch `main` will be used. The arguemnt is specified via `-b`.
* An app must be specified via the `-a` to indicate which app you wish to rollback. 

### rollback_local
    ❯ python manage.py rollback_local -a polls 
    
* An app must be specified via the `-a` to indicate which app you wish to rollback. 
* This will simply migrate back to the previous migration.

## Installing
### From GitHub
    ❯ pip install git+ssh://git@github.com/jdboisvert/django-migration-rollback

### From [PyPI](https://pypi.org/project/mighty-bedmas-calculator/2022.7.26.0/#description)
    ❯ pip install mighty-bedmas-calculator==2022.7.26.0

### Quick start 
Add "migration_rollback" to your INSTALLED_APPS in the `settings.py` like this:
```
    INSTALLED_APPS = [
        ...
        'migration_rollback',
    ]
```