from subprocess import STDOUT, Popen, PIPE


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
    Gets the previous migration present in an app's migration directory in the database

    :param app_name: The name of the app to get the previous migration for
    :return: The previous migration number (ex: 0001 for 0001_initial.py)
    """
    command = f"python manage.py showmigrations {app_name} 2>/dev/null | sort -r | grep '\[X\]' | head -2 | tail -1 | cut -d ' ' -f 3"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)

    return command_pipe.stdout.read().decode("utf-8").split("_")[0]
