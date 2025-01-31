# Django Stars Backend Skeleton

[Django](https://www.djangoproject.com/) project template based on [cookiecutter](https://cookiecutter.readthedocs.io/).

Project preconfigured with best practices and tools to work from the box with minimal configuration and setup. 
Fast start achieved by using docker and docker compose.

## What's included

* Settings via environment variables with [django-environ](https://django-environ.readthedocs.io/).
* [Celery](http://www.celeryproject.org/) configuration.
* [Django REST Framework](https://www.django-rest-framework.org/) configuration + Swagger with [drf-spectacular](https://drf-spectacular.readthedocs.io/).
* Typical user CRUD APIs.
* Docker support using [docker-compose](https://docs.docker.com/compose/) configuration for local development (incl. [Postgres](https://www.postgresql.org/), [Redis](https://redis.io/) & [MailPit](https://github.com/axllent/mailpit) for testing emails).
* Requirements management with [poetry](https://python-poetry.org/).
* [pytest](https://docs.pytest.org/) configuration.
* Code formatting with [Ruff](https://docs.astral.sh/ruff/formatter/).
* Checking code with [Ruff](https://docs.astral.sh/ruff/) - which includes _flake8_, _isort_, _bandit_, _pylint_ etc.
* [Pre-commit](https://pre-commit.com/) hook for running test & linters on each commit.
* Integration with [Sentry](https://sentry.io/).

## How to use

### Prerequisites
Installed [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html) and [docker](https://docs.docker.com/engine/install/)

### Set up project
Step into directory you want to create project and generate project with cookiecutter:

```bash
cd /path/to/directory
cookiecutter https://github.com/django-stars/backend-skeleton
```
Answer the questions in wizard.

### Steps after project setup

Step into directory of your project.

Copy `.env` file from example file:

```bash
cp ./api/.env.example ./api/.env
```

Run application:

```bash
make compose-up
```

We are using docker for running the app, so you don't have to keep your python env locally. 
But we also use pre-commit hooks, and the `safety` hook requires `poetry` to be in your `PATH`.

> [!TIP]
> Ensure the poetry installed with the same python version as in `pyproject.toml`
