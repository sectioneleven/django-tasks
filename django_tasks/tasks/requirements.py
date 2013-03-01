import os

from fabric.api import task, local


@task
def install(env=os.environ.get("DJANGO_ENV", "development")):
    """Installs the packages defined in the requirements file for the given
    environment [development, production].
    """
    if env == "development":
        local("pip install -r requirements/development.txt")
    else:
        local("pip install -r requirements.txt")
