from setuptools import setup, find_packages
from django_tasks import __version__

setup(
    name='django-tasks',
    version=__version__,
    description='Tasks for django.',
    author='Warren Chua & Lemuel Formacil',
    author_email='lemuelf@gmail.com',
    packages=find_packages(),
    install_requires=['Fabric>=1.5.3']
)
