from fabric.api import task, local, abort
from fabric.contrib.console import confirm

from fabric.contrib import django
django.project("online_store")

from django.conf import settings

@task
def create(dbalias="default"):
    """Creates the database defined for the supplied [dbalias] argument, or
    the 'default' database if no arguments were given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # createdb -E utf8 -O database["USER"] database["NAME"]
    local("createdb -e -E utf8 -O %s %s" % (settings_dict["USER"], settings_dict["NAME"]))

@task
def drop(dbalias="default"):
    """Drops the database defined for the supplied [dbalias] argument, or the
    'default' database if no argument were given.
    """
    settings_dict = settings.DATABASES[dbalias]

    # dropdb -U database["USER"] database["NAME"]
    if not confirm("Are you sure you want to drop the database \"%s\"?" % settings_dict["NAME"], default=False):
        abort("Cancelled.")
    local("dropdb -e -U %s %s" % (settings_dict["USER"], settings_dict["NAME"]))
