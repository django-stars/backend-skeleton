from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def pip_compile(ctx):
    with ctx.cd(project_path("api")):
        command_build = "pip-compile --upgrade --generate-hashes -o ./requirements-build.txt ./requirements-build.in"
        command_dev = "pip-compile --upgrade --generate-hashes -o ./requirements-dev.txt ./requirements-dev.in"
        ctx.run(command_build, pty=True, replace_env=False)
        ctx.run(command_dev, pty=True, replace_env=False)


@task()
def pip_sync(ctx):
    with ctx.cd(project_path("api")):
        ctx.run("pip-sync ./requirements-dev.txt", pty=True, replace_env=False)


pip_collection = Collection("pip")
pip_collection.add_task(pip_compile, name="compile")
pip_collection.add_task(pip_sync, name="sync")
