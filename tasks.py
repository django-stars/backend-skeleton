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


@task()
def test_project(ctx):
    rmtree("build", ignore_errors=True)
    ctx.run("cookiecutter --no-input --overwrite-if-exists --output-dir build .", pty=True, replace_env=False)
    project_path = path("build", "awesome", "api")
    virtual_env_path = path("build", ".env")
    env_variables = " ".join(
        (
            "AWESOME_SECRET_KEY=test-secret-key",
            "AWESOME_EMAIL_BACKEND=django.core.mail.backends.dummy.EmailBackend",
            "AWESOME_USE_SENTRY=off",
            "AWESOME_DEBUG=off",
            "AWESOME_DATABASE_URL=postgresql://postgres@localhost/awesome_test_db",
            "AWESOME_CELERY_BROKER=redis://localhost:6379/1",
            "AWESOME_CELERY_TASK_ALWAYS_EAGER=on",
        )
    )
    with ctx.cd(project_path):
        ctx.run(f"python3 -m venv {virtual_env_path}", pty=True, replace_env=True)
        ctx.run(f"{virtual_env_path}/bin/pip install -U pip fabric invoke pip-tools", pty=True, replace_env=True)
        ctx.run(f"""source {virtual_env_path}/bin/activate && \
{virtual_env_path}/bin/fab pip.compile && \
{virtual_env_path}/bin/fab pip.sync && \
{env_variables} {virtual_env_path}/bin/fab test.black-apply && \
{env_variables} {virtual_env_path}/bin/fab test.isort-apply && \
{env_variables} {virtual_env_path}/bin/fab test.all""", pty=True, replace_env=True)


compose_collection = Collection("compose")
compose_collection.add_task(compose_up, name="up")
compose_collection.add_task(compose_down, name="down")
pip_collection = Collection("pip")
pip_collection.add_task(pip_compile, name="compile")
pip_collection.add_task(pip_sync, name="sync")
test_collection = Collection("test")
test_collection.add_task(test_hooks, name="hooks")
test_collection.add_task(test_project, name="project")
namespace = Collection(compose_collection, pip_collection, test_collection, )
