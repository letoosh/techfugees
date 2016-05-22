import sys

from fabric.api import (local, put, cd, run, env, roles,
                        execute, sudo, hosts, reboot,
                        prompt, settings, hide)

from fabric.context_managers import shell_env
from fabric.colors import red, green

from ansible.inventory import Inventory

# TODO: Change this so these settings
# are read automatically from the ansible configuration files.
# This invlolves reading production/staging.yml and webserver
# role configuration to extract the correct variables. For now
# we rely on convention
APP_NAME = "techfugees"
APP_USER = "techfugees"
SSH_USER = "ubuntu"
REPO_PATH = "/srv/" + APP_NAME
DJANGO_PATH = REPO_PATH + "/" + APP_NAME
VIRTUALENV_PATH = "/home/{app_user}/.{app_name}/".format(
    app_user=APP_USER, app_name=APP_NAME
)
PIP_BINARY = VIRTUALENV_PATH + "bin/pip"
PYTHON_BINARY = VIRTUALENV_PATH + "bin/python"

env.use_ssh_config = True

@roles("webservers")
def pull():
    with cd(REPO_PATH):
        sudo("git pull", user=APP_USER)
    print(green('updated git repository'))


@roles("webservers")
def branch(branch):
    with cd(REPO_PATH):
        sudo(
            "git checkout {branch}".format(branch=branch),
            user=APP_USER)
    print(green('changed git branch to `{branch}`'.format(branch=branch)))


@roles("webservers")
def stash():
    with cd(REPO_PATH):
        sudo("git stash", user=APP_USER)
    print(green('stashed current changes'))


@roles("webservers")
def unstash():
    with cd(REPO_PATH):
        sudo("git stash apply", user=APP_USER)
    print(green('unstashed current changes'))


@roles("webservers")
def update_ve():
    with cd(REPO_PATH):
        sudo("{pip} install -r requirements/{requirements}".format(
             pip=PIP_BINARY,
             requirements=env.REQUIREMENTS_FILE),
             user=APP_USER)
    print(green('updated virtual enviroment'))


@roles("webservers")
def migrate():
    with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
        with cd(DJANGO_PATH):
            sudo("{python} manage.py migrate".format(
                 python=PYTHON_BINARY),
                 user=APP_USER)
    print(green('migrated DB to be up to date with branch'))


@roles("webservers")
def collectstatic():
    with shell_env(DJANGO_SETTINGS_MODULE=env.DJANGO_SETTINGS_MODULE):
        with cd(DJANGO_PATH):
            sudo("{python} manage.py collectstatic --noinput".format(
                 python=PYTHON_BINARY),
                 user=APP_USER)
            sudo("{python} manage.py assets build".format(
                 python=PYTHON_BINARY),
                 user=APP_USER)
    print(green('collected static files and rebuilt assets'))


@roles("webservers")
def restart_all():
    sudo('supervisorctl restart all')
    print(green('restarted all supervisor processes'))


@roles("webservers")
def stop_all():
    sudo('supervisorctl stop all')
    print(green('stopped all supervisor processes'))


@roles("webservers")
def start_all():
    sudo('supervisorctl start all')
    print(green('started all supervisor processes'))


@roles("webservers")
def start(process):
    sudo('supervisorctl start {process}'.format(process=process))
    print(green('started the `{process}` supervisor process'.format(process=process)))


@roles("webservers")
def restart(process):
    sudo('supervisorctl restart {process}'.format(process=process))
    print(green('restarted the `{process}` supervisor process'.format(process=process)))


@roles("webservers")
def stop(process):
    sudo('supervisorctl stop {process}'.format(process=process))
    print(green('stopped the `{process}` supervisor process'.format(process=process)))


def production():
    prompt(red("Are you sure you want to run on production? [y/n]"), validate=validate_yes_no)

    inventory = Inventory('ansible/production')

    env.roledefs={
        "webservers": [
            "{ssh_user}@{address}".format(
                ssh_user=SSH_USER,
                address=host.name
            )
            for host in inventory.get_group('webservers').hosts
        ]
    }

    env.DJANGO_SETTINGS_MODULE = "techfugees.settings.production"
    env.REQUIREMENTS_FILE = "production.txt"
    env.PROVISION_ENV = "production"


def staging():
    inventory = Inventory('ansible/staging')

    env.roledefs={
        "webservers": [
            "{ssh_user}@{address}".format(
                ssh_user=SSH_USER,
                address=host.name
            )
            for host in inventory.get_group('webservers').hosts
        ]
    }

    env.DJANGO_SETTINGS_MODULE = "techfugees.settings.staging"
    env.REQUIREMENTS_FILE = "staging.txt"
    env.PROVISION_ENV = "staging"


def deploy():

    execute(pull)
    execute(update_ve)
    execute(migrate)
    execute(collectstatic)
    execute(restart_all)


def validate_yes_no(val):
    if val.lower() != "y":
        print(red("Exiting"))
        sys.exit(0)
    return val.lower()


def coerce_bool(val):
    return val == "True"


def provision(check="False"):
    check = coerce_bool(check)
    if check:
        check_string = "--check"
    else:
        check_string = ""
        prompt("Are you sure you want to provision the %s servers? They will be stopped before provisioning occurs. (Y/N):" % env.PROVISION_ENV, default="N", validate=validate_yes_no)

    if not check:
        try:
            execute(stop_all)
        except:
            print(red("Exception while stopping the processes"))
            prompt("Is this the first time you are provision this server? (Y/N):",
                   default="N", validate=validate_yes_no)

    local(
        "ansible-playbook ansible/{env}.yml -k -i ansible/{env} -vvvv -u {ssh_user} {check} --diff".format(
            ssh_user=SSH_USER,
            env=env.PROVISION_ENV,
            check=check_string))
    execute(start_all)
