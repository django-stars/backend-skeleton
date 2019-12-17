from invoke import Collection  # isort:skip

from fabric_scripts.backend import backend_clean_pyc, backend_run, backend_shell
from fabric_scripts.celery import celery_collection
from fabric_scripts.compose import compose_collection
from fabric_scripts.frontend import frontend_collection
from fabric_scripts.git import git_collection
from fabric_scripts.pip_tools import pip_collection
from fabric_scripts.test import test_collection


namespace = Collection(
    celery_collection,
    compose_collection,
    frontend_collection,
    git_collection,
    pip_collection,
    test_collection,
)
namespace.add_task(backend_run, name="run")
namespace.add_task(backend_shell, name="shell")
namespace.add_task(backend_clean_pyc, name="clean-pyc")
