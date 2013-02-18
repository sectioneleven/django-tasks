from . import (db, requirements)
from fabric.api import task, local

@task
def setup():
	"""Sets up the project."""
	requirements.install()
	db.init()

@task
def update():
	"""Updates the project from origin."""
	local("git pull origin master")
	local("git stash")
	local("git rebase master")
	local("git stash pop")
	local("./manage.py migrate")
