import re
from subprocess import STDOUT, Popen, PIPE
from typing import List

_SAFE_NAME_RE = re.compile(r'^[a-zA-Z0-9_\-/.]+$')

from django.db import connection
from django.db.migrations.loader import MigrationLoader

DJANGO_SYSTEM_APPS = frozenset(["admin", "auth", "contenttypes", "sessions"])


def get_all_migrated_app_names(include_system_apps: bool = False) -> List[str]:
    """
    Gets the names of all apps that have at least one applied migration.

    :param include_system_apps: Include Django system apps (auth, admin, contenttypes, sessions).
                                Defaults to False so rollback-all does not accidentally touch them.
    :return: A list of app names with applied migrations
    """
    loader = MigrationLoader(connection)
    seen = set()
    app_names = []
    for (app_label, _) in loader.applied_migrations:
        if app_label not in seen:
            seen.add(app_label)
            if include_system_apps or app_label not in DJANGO_SYSTEM_APPS:
                app_names.append(app_label)
    return app_names


def get_latest_migration_in_git(app_name: str, branch_name: str) -> str:
    """
    Gets the latest migration present in an app's migration directory in git

    :param app_name: The name of the app to get the latest migration for
    :param branch_name: The name of the branch to get the latest migration from
    :return: The latest migration number (ex: 0001 for 0001_initial.py)
    :raises ValueError: If app_name or branch_name contain unsafe characters
    """
    if not _SAFE_NAME_RE.match(app_name):
        raise ValueError(f"Invalid app_name {app_name!r}: only alphanumeric characters, underscores, hyphens, dots, and slashes are allowed.")
    if not _SAFE_NAME_RE.match(branch_name):
        raise ValueError(f"Invalid branch_name {branch_name!r}: only alphanumeric characters, underscores, hyphens, dots, and slashes are allowed.")

    command = f"git ls-tree -r {branch_name} --name-only | grep \"{app_name}/migrations/[0].*\" | sort -r | head -1 | cut -d / -f 3 | sed 's/.py$//'"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    migration_number = command_pipe.stdout.read().decode("utf-8").strip().split("_")[0]

    return migration_number


def get_previous_migration(app_name: str) -> str:
    """
    Gets the previous applied migration for an app from the database.

    :param app_name: The name of the app to get the previous migration for
    :return: The previous migration number (ex: 0001 for 0001_initial.py)
    """
    loader = MigrationLoader(connection)
    applied = sorted(migration_name for (app_label, migration_name) in loader.applied_migrations if app_label == app_name)

    if len(applied) < 2:
        return ""

    return applied[-2].split("_")[0]
