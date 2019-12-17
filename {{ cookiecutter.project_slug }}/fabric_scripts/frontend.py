from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def frontend_build(ctx):
    with ctx.cd(project_path("client")):
        ctx.run("yarn install", pty=True, replace_env=False)
        ctx.run("yarn build", pty=True, replace_env=False)


@task()
def frontend_start(ctx):
    with ctx.cd(project_path("client")):
        ctx.run("yarn install", pty=True, replace_env=False)
        ctx.run("yarn start", pty=True, replace_env=False)


frontend_collection = Collection("fe")
frontend_collection.add_task(frontend_build, name="build")
frontend_collection.add_task(frontend_start, name="start")
