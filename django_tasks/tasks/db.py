import os
import pwd

from fabric.api import task, local, abort
from fabric.contrib.console import confirm

from django.conf import settings
from django.db.utils import DEFAULT_DB_ALIAS


def use_sudo_p():
    return get_username() != get_pg_user()


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def get_pg_user():
    return local("ps aux | grep 'postgres -D' | grep -v grep", True).split("\n")[0].split()[0]


@task
def create(dbalias=DEFAULT_DB_ALIAS):
    """Creates the database defined for the supplied [dbalias] argument, or
    the 'default' database if no argument was given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # createdb -E utf8 -O database["USER"] database["NAME"]
    cmd = "createdb -e -E utf8 -O %s %s" % (settings_dict["USER"], settings_dict["NAME"])
    if use_sudo_p():
        cmd = "sudo su %s -c '%s'" % (get_pg_user(), cmd)
    local(cmd)


@task
def drop(dbalias=DEFAULT_DB_ALIAS):
    """Drops the database defined for the supplied [dbalias] argument, or the
    'default' database if no argument was given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # dropdb -U database["USER"] database["NAME"]
    if not confirm("Are you sure you want to drop the database \"%s\"?" % settings_dict["NAME"], default=False):
        abort("Cancelled.")
    cmd = "dropdb -e %s" % (settings_dict["NAME"])
    if use_sudo_p():
        cmd = "sudo su %s -c '%s'" % (get_pg_user(), cmd)
    local(cmd)


@task
def create_user(dbalias=DEFAULT_DB_ALIAS):
    """Creates the database user.
    """
    settings_dict = settings.DATABASES[dbalias]

    # createuser -e -d -R -S database["USER"]
    cmd = "createuser -e -d -R -S %s" % (settings_dict["USER"])
    if use_sudo_p():
        cmd = """sudo su %s -c "psql -c \\"CREATE USER %s WITH CREATEDB%s;\\"" """ % (get_pg_user(), settings_dict["USER"], (" ENCRYPTED PASSWORD '%s'" % (settings_dict["PASSWORD"])) if len(settings_dict["PASSWORD"]) > 0 else "")
    local(cmd)


@task
def drop_user(dbalias=DEFAULT_DB_ALIAS):
    """Drops the database user.
    """
    settings_dict = settings.DATABASES[dbalias]

    # dropuser -e database["USER"]
    cmd = "dropuser -e %s" % (settings_dict["USER"])
    if use_sudo_p():
        cmd = "sudo su %s -c '%s'" % (get_pg_user(), cmd)
    local(cmd)


@task
def init(dbalias=DEFAULT_DB_ALIAS):
    """Initialize the database.

    Creates the database user and the database.
    """
    create_user(dbalias)
    create(dbalias)
    local("./manage.py syncdb")
    local("./manage.py migrate")


@task
def reset(dbalias=DEFAULT_DB_ALIAS):
    """Resets the database.

    Drops the database and then re-creates it.
    """
    drop(dbalias)
    create(dbalias)
    local("./manage.py syncdb --noinput")
    local("./manage.py migrate")
    local("./manage.py loaddata online_store/fixtures/*")
