from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def celery_all(ctx):
    with ctx.cd(project_path("api")):
        ctx.run(
            "celery -A {{ cookiecutter.project_slug }} worker -l DEBUG --beat",
            pty=True,
            replace_env=False,
        )


@task()
def celery_worker(ctx):
    with ctx.cd(project_path("api")):
        ctx.run(
            "celery -A {{ cookiecutter.project_slug }} worker -l DEBUG",
            pty=True,
            replace_env=False,
        )


@task()
def celery_beat(ctx):
    with ctx.cd(project_path("api")):
        ctx.run(
            "celery -A {{ cookiecutter.project_slug }} beat -l DEBUG",
            pty=True,
            replace_env=False,
        )


@task()
def celery_clear_queue(ctx):
    with ctx.cd(project_path("api")):
        ctx.run(
            "celery -A {{ cookiecutter.project_slug }} purge -f",
            pty=True,
            replace_env=False,
        )


celery_collection = Collection("celery")
celery_collection.add_task(celery_all, name="all")
celery_collection.add_task(celery_worker, name="worker")
celery_collection.add_task(celery_beat, name="beat")
celery_collection.add_task(celery_clear_queue, name="clear")
