from subprocess import STDOUT, Popen, PIPE

def get_latest_migration_in_git(app_name: str, branch_name: str):
    """ Gets the latest migration present in an app's migration folder on git """
    command = f"git ls-tree -r {branch_name} --name-only | grep \"{app_name}/migrations/[0].*\" | sort -r | head -1 | cut -d / -f 3 | sed 's/.py$//'"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    migration_number = command_pipe.stdout.read().decode("utf-8").split("_")[0]
    
    return migration_number

def get_previous_migration(app_name: str):
    """ Get the previously applied migration """
    command = f"python manage.py showmigrations {app_name} | sort -r | grep '\[X\]' | head -2 | tail -1 | cut -d ' ' -f 3"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    mirgration = command_pipe.stdout.read().decode("utf-8")
        
    return mirgration
    
def rollback(app_name: str, migration: str):
    """ Migrate a given app to the given migration """
    command = f"python manage.py migrate {app_name} {migration}"
    command_pipe = Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    command_pipe.stdout.read().decode("utf-8")