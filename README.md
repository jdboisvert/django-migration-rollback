# Django Migration Rollback v1.0.5
A Django package used to just make the `python manage.py migrate` a little easier for Django apps that commit their migrations and want a way to rollback to a previous migration without needing to check what the which one it is via `python manage.py showmigrations` or in the project's git repository.

## Features
Able to set which branch in a git repository to rollback to using the custom command `migraterollback` or if you wish to just rollback to a previous migration only via `migrateprevious`. Note in order to use the rollback with a git repository's branch feature with git the project must have a `.git` file present.

### Django `migraterollback` command
    ❯ python manage.py migraterollback polls feature/really-cool-branch
    Attempting to go back to rollback polls to latest migration on branch feature/really-cool-branch
    Operations to perform:
        Target specific migration: 0006_question5, from polls
    Running migrations:
        Rendering model states...
    DONE
        Unapplying polls.0007_question6...
    OK

This command is used to migrate a Django app back to the migration found in a repository's branch (this will also migrate to that migration if behind).

* An app must be specified as the first argument after the command to indicate which app you wish to rollback.
* By default if no argument is specified after the app, the branch `main` will be used.

### Django `migrateprevious` command
    ❯ python manage.py migrateprevious polls
    Attempting to go back to rollback polls to previous migration
    Operations to perform:
        Target specific migration: 0005_question4, from polls
    Running migrations:
        Rendering model states...
    DONE
        Unapplying polls.0006_question5...
    OK

This command is used to migrate a Django app back to the previously applied migration.

* An app must be specified as the first argument after the command to indicate which app you wish to migrate to the previously applied migration.

## Installing
### From PyPi
```
pip install django-migration-rollback
```

### From GitHub
```
pip install git+ssh://git@github.com/jdboisvert/django-migration-rollback
```

### Quick start
Add "migration_rollback" to your INSTALLED_APPS in the `settings.py` like this:
```
    INSTALLED_APPS = [
        ...
        'migration_rollback',
    ]
```

### Development

## Getting started
```bash
# install pyenv (if necessary)
brew install pyenv pyenv-virtualenv
echo """
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
""" > ~/.zshrc
source ~/.zshrc

# create a virtualenv
pyenv install 3.10.5
pyenv virtualenv 3.10.5 django_migration_rollback
pyenv activate django_migration_rollback

# install dependencies
pip install -U pip
pip install -r requirements.txt -r requirements_dev.txt
```

## Installing pre-commit hooks
```bash
pre-commit install
```
