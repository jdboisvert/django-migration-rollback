from subprocess import STDOUT, Popen, PIPE

def get_latest_migration_in_git(app_name: str, branch_name: str):
    """ Gets the latest migration present in an app's migration folder on git """
    command = f"git ls-tree -r {branch_name} --name-only | grep \"{app_name}/migrations/[0].*\" | sort -r | head -1 | cut -d / -f 3 | sed 's/.py$//'"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    migration_number = command_pipe.stdout.read().decode("utf-8").split("_")
    
    return migration_number

def get_previous_migration(app_name: str):
    """ Get the previously applied migration """
    # TODO test in a Django app
    command = f"python manage.py showmigrations {app_name} | grep '\[X\]'"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    mirgration = command_pipe.stdout.read().decode("utf-8")
    
    print(mirgration)
    
    
def rollback(app_name: str, migration: str):
    """ Migrate a given app to the given migration """
    command = f"python manage.py migrate {app_name} {migration}"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    migrate_data = command_pipe.stdout.read().decode("utf-8")
    
    print(migrate_data)