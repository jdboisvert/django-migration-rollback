from subprocess import STDOUT, Popen, PIPE
from typing import List

from django.db import connection
from django.db.migrations.loader import MigrationLoader


def get_all_migrated_app_names() -> List[str]:
    """
    Gets the names of all apps that have at least one applied migration.

    :return: A list of app names with applied migrations
    """
    loader = MigrationLoader(connection)
    seen = set()
    app_names = []
    for (app_label, _) in loader.applied_migrations:
        if app_label not in seen:
            seen.add(app_label)
            app_names.append(app_label)
    return app_names


def get_latest_migration_in_git(app_name: str, branch_name: str) -> str:
    """
    Gets the latest migration present in an app's migration directory in git

    :param app_name: The name of the app to get the latest migration for
    :param branch_name: The name of the branch to get the latest migration from
    :return: The latest migration number (ex: 0001 for 0001_initial.py)
    """
    command = f"git ls-tree -r {branch_name} --name-only | grep \"{app_name}/migrations/[0].*\" | sort -r | head -1 | cut -d / -f 3 | sed 's/.py$//'"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    migration_number = command_pipe.stdout.read().decode("utf-8").split("_")[0]

    return migration_number


def get_previous_migration(app_name: str) -> str:
    """
    Gets the previous applied migration for an app from the database.

    :param app_name: The name of the app to get the previous migration for
    :return: The previous migration number (ex: 0001 for 0001_initial.py)
    """
    loader = MigrationLoader(connection)
    applied = sorted(
        migration_name
        for (app_label, migration_name) in loader.applied_migrations
        if app_label == app_name
    )

    if len(applied) < 2:
        return ""

    return applied[-2].split("_")[0]
