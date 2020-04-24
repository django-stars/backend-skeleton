from fabric import task
from invoke import Collection

from ._common import project_path


@task()
def test_run(ctx, module=None):
    with ctx.cd(project_path("api")):
        pytest_command_args = [
            "pytest",
            "--cache-clear",
            "--capture=no",
            "--showlocals",
            "--verbose",
            "--cov={{ cookiecutter.project_slug }}",
            "--cov-report html",
            "--no-migrations",
            "--junitxml",
            "./test-results/test-results.xml",
        ]
        if module:
            pytest_command_args.append(module)
        ctx.run(" ".join(pytest_command_args), pty=True, replace_env=False)


@task()
def test_bandit(ctx):
    with ctx.cd(project_path()):
        ctx.run("bandit -r .", pty=True, replace_env=False)


@task()
def test_black_check(ctx):
    with ctx.cd(project_path()):
        ctx.run("black --check .", pty=True, replace_env=False)


@task()
def test_black_apply(ctx):
    with ctx.cd(project_path()):
        ctx.run("black .", pty=True, replace_env=False)


@task()
def test_isort_check(ctx):
    with ctx.cd(project_path()):
        ctx.run("isort --check --skip .env", pty=True, replace_env=False)


@task()
def test_isort_apply(ctx):
    with ctx.cd(project_path()):
        ctx.run("isort --apply --skip .env", pty=True, replace_env=False)


@task()
def test_pylama(ctx):
    with ctx.cd(project_path("api")):
        ctx.run("pylama", pty=True, replace_env=False)


@task()
def test_pylint(ctx):
    with ctx.cd(project_path("api")):
        ctx.run("pylint --ignore=tests {{ cookiecutter.project_slug }}", pty=True, replace_env=False)


@task()
def test_safety(ctx):
    ctx.run("safety check", pty=True, replace_env=False)


@task()
def test_all(ctx):
    test_run(ctx)
    test_black_check(ctx)
    test_isort_check(ctx)
    test_bandit(ctx)
    test_pylama(ctx)
    test_pylint(ctx)
    test_safety(ctx)


test_collection = Collection("test")
test_collection.add_task(test_run, name="run")
test_collection.add_task(test_all, name="all")
test_collection.add_task(test_black_check, name="black")
test_collection.add_task(test_black_apply, name="black-apply")
test_collection.add_task(test_bandit, name="bandit")
test_collection.add_task(test_isort_check, name="isort")
test_collection.add_task(test_isort_apply, name="isort-apply")
test_collection.add_task(test_pylama, name="pylama")
test_collection.add_task(test_pylint, name="pylint")
test_collection.add_task(test_safety, name="safety")
