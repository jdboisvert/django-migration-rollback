# Django Migration Rollback v1.1.0
A Django package used to just make the `python manage.py migrate` a little easier for Django apps that commit their migrations and want a way to rollback to a previous migration without needing to check what the which one it is via `python manage.py showmigrations` or in the project's git repository.

## Features

- Roll back a single app or **all apps at once**
- Roll back to the migration matching a specific git branch (`migraterollback`)
- Roll back to the previously applied migration (`migrateprevious`)
- `--fake` / `--fake-initial` support for marking migrations without running them
- `--yes` / `-y` flag to skip confirmation prompts (useful in CI)
- `--include-system-apps` to include Django's built-in apps in bulk rollbacks

---

## Commands

### `migraterollback`

Rolls back a Django app's migrations to match the latest migration found on a given git branch.

**Roll back a single app:**
```
❯ python manage.py migraterollback polls feature/really-cool-branch
Attempting to rollback polls to latest migration on branch 'feature/really-cool-branch'
Operations to perform:
    Target specific migration: 0006_question5, from polls
Running migrations:
    Rendering model states... DONE
    Unapplying polls.0007_question6... OK
```

**Roll back all apps to match a branch (with confirmation prompt):**
```
❯ python manage.py migraterollback main
The following apps will be rolled back to the latest migration on branch 'main':
  - polls
  - accounts

Are you sure you want to continue? [y/N] y
Rolling back all apps to latest migration on branch 'main'
...
```

**Skip the confirmation prompt (useful in CI):**
```
❯ python manage.py migraterollback main --yes
```

**Mark migrations as applied without running them:**
```
❯ python manage.py migraterollback polls feature/really-cool-branch --fake
```

**Include Django system apps (auth, admin, etc.) in a bulk rollback:**
```
❯ python manage.py migraterollback main --include-system-apps
```
> **Warning:** System apps have cross-app dependencies. Rolling them back can cause cascading effects. Use with caution.

#### Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `app` | No | — | App to roll back. Omit to roll back all non-system apps. |
| `branch` | No | `main` | Git branch to roll back to. |
| `--fake` | No | `False` | Mark the target migration as applied without running SQL. |
| `--fake-initial` | No | `False` | Fake-apply the initial migration if its tables already exist. |
| `--yes` / `-y` | No | `False` | Skip the confirmation prompt when rolling back all apps. |
| `--include-system-apps` | No | `False` | Include `auth`, `admin`, `contenttypes`, `sessions` in bulk rollback. |

---

### `migrateprevious`

Rolls back a Django app's migrations to the previously applied migration.

**Roll back a single app:**
```
❯ python manage.py migrateprevious polls
Attempting to rollback polls to previous migration
Operations to perform:
    Target specific migration: 0005_question4, from polls
Running migrations:
    Rendering model states... DONE
    Unapplying polls.0006_question5... OK
```

**Roll back all apps to their previous migration:**
```
❯ python manage.py migrateprevious
The following apps will be rolled back to their previous migration:
  - polls
  - accounts

Are you sure you want to continue? [y/N] y
Rolling back all apps to their previous migration
...
```

**Skip the confirmation prompt:**
```
❯ python manage.py migrateprevious --yes
```

**Mark migrations as applied without running them:**
```
❯ python manage.py migrateprevious polls --fake
```

#### Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `app` | No | — | App to roll back. Omit to roll back all non-system apps. |
| `--fake` | No | `False` | Mark the target migration as applied without running SQL. |
| `--fake-initial` | No | `False` | Fake-apply the initial migration if its tables already exist. |
| `--yes` / `-y` | No | `False` | Skip the confirmation prompt when rolling back all apps. |
| `--include-system-apps` | No | `False` | Include `auth`, `admin`, `contenttypes`, `sessions` in bulk rollback. |

---

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
```python
INSTALLED_APPS = [
    ...
    'migration_rollback',
]
```

---

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
pyenv install 3.11.0
pyenv virtualenv 3.11.0 django_migration_rollback
pyenv activate django_migration_rollback

# install dependencies
pip install -U pip
pip install -r requirements.txt -r requirements_dev.txt
```

## Installing pre-commit hooks
```bash
pre-commit install
```
