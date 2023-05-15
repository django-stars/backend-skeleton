import os
from shutil import rmtree

from invoke import Collection, task


def path(*args):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, *args)


@task()
def compose_up(ctx, daemon=False):
    with ctx.cd(path("contrib", "docker")):
        command = "docker-compose --file docker-compose-local.yml --project-name=awesome up"
        if daemon:
            command = f"{command} -d"
        ctx.run(command, pty=True, replace_env=False)


@task()
def compose_down(ctx, volumes=False):
    with ctx.cd(path("contrib", "docker")):
        command = "docker-compose --file docker-compose-local.yml --project-name=awesome down"
        if volumes:
            command = f"{command} -v"
        ctx.run(command, pty=True, replace_env=False)


@task()
def pip_compile(ctx):
    command = "pip-compile --upgrade --generate-hashes -o ./requirements.txt ./requirements.in"
    ctx.run(command, pty=True)


@task()
def pip_sync(ctx):
    ctx.run("pip-sync ./requirements.txt", pty=True)


@task()
def test_hooks(ctx):
    ctx.run("pytest -s --cov=hooks --cov-report=html", pty=True, replace_env=False)


compose_collection = Collection("compose")
compose_collection.add_task(compose_up, name="up")
compose_collection.add_task(compose_down, name="down")
pip_collection = Collection("pip")
pip_collection.add_task(pip_compile, name="compile")
pip_collection.add_task(pip_sync, name="sync")
test_collection = Collection("test")
test_collection.add_task(test_hooks, name="hooks")
namespace = Collection(compose_collection, pip_collection, test_collection, )
