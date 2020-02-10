from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def compose_up(ctx, daemon=False):
    with ctx.cd(project_path("docker")):
        command = "docker-compose --file docker-compose-local.yml --project-name={{ cookiecutter.project_slug }} up"
        if daemon:
            command = f"{command} -d"
        ctx.run(command, pty=True, replace_env=False)


@task()
def compose_down(ctx, volumes=False):
    with ctx.cd(project_path("docker")):
        command = "docker-compose --file docker-compose-local.yml --project-name={{ cookiecutter.project_slug }} down"
        if volumes:
            command = f"{command} -v"
        ctx.run(command, pty=True, replace_env=False)


compose_collection = Collection("compose")
compose_collection.add_task(compose_up, name="up")
compose_collection.add_task(compose_down, name="down")
