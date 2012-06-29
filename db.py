from fabric.api import task, local, abort
from fabric.contrib.console import confirm

from django.conf import settings
from django.db.utils import DEFAULT_DB_ALIAS

@task
def create(dbalias=DEFAULT_DB_ALIAS):
    """Creates the database defined for the supplied [dbalias] argument, or
    the 'default' database if no argument was given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # createdb -E utf8 -O database["USER"] database["NAME"]
    local("createdb -e -E utf8 -O %s %s" % (settings_dict["USER"], settings_dict["NAME"]))

@task
def drop(dbalias=DEFAULT_DB_ALIAS):
    """Drops the database defined for the supplied [dbalias] argument, or the
    'default' database if no argument was given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # dropdb -U database["USER"] database["NAME"]
    if not confirm("Are you sure you want to drop the database \"%s\"?" % settings_dict["NAME"], default=False):
        abort("Cancelled.")
    local("dropdb -e -U %s %s" % (settings_dict["USER"], settings_dict["NAME"]))

@task
def create_user(dbalias=DEFAULT_DB_ALIAS):
    """Creates the database user.
    """
    settings_dict = settings.DATABASES[dbalias]

    # createuser -e -d -R -S database["USER"]
    local("createuser -e -d -R -S %s" % (settings_dict["USER"]))

@task
def drop_user(dbalias=DEFAULT_DB_ALIAS):
    """Drops the database user.
    """
    settings_dict = settings.DATABASES[dbalias]

    # dropuser -e database["USER"]
    local("dropuser -e %s" % (settings_dict["USER"]))

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
    local("./manage.py syncdb")
    local("./manage.py migrate")
