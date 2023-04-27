# Django Stars Backend Skeleton

[Django](https://www.djangoproject.com/) project template based on [cookiecutter](https://cookiecutter.readthedocs.io/).

## What's included

* Settings via environment variables with [django-environ](https://django-environ.readthedocs.io/).
* [Celery](http://www.celeryproject.org/) configuration.
* [Django REST Framework](https://www.django-rest-framework.org/) configuration + Swagger with [drf-yasg](https://drf-yasg.readthedocs.io/).
* Typical user CRUD APIs.
* Simple [docker-compose](https://docs.docker.com/compose/) configuration for local development (incl. [Postgres](https://www.postgresql.org/), [Redis](https://redis.io/) & [MailHog](https://github.com/mailhog/MailHog) for testing emails).
* Requirements management with [pip-tools](https://pypi.org/project/pip-tools/).
* [pytest](https://docs.pytest.org/) configuration.
* Code formatting with [Black](https://black.readthedocs.io/).
* Checking code with [Ruff](https://beta.ruff.rs/docs/) - which includes _flake8_, _isort_ etc.
* [Pre-commit](https://pre-commit.com/) hook for running test & linters on each commit.
* Integration with [Sentry](https://sentry.io/).

## How to use

Create python virtual environment. We recommend to use [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):

```bash
pyenv install 3.9.5
pyenv virtualenv 3.9.5 my_project
pyenv activate my_project
```

Install cookiecutter and packaging:

```bash
pip install cookiecutter packaging
```

Step into directory you want to create project and generate project with cookiecutter:

```bash
cd /path/to/directory
cookiecutter https://github.com/django-stars/backend-skeleton
```

Answer the questions in wizard.

## Steps after project setup

Install tools required to build a dependencies list:

```bash
pip install -U fabric invoke pip pip-tools
```

Run backing services:

```bash
make compose-up
```

Copy `.env` file from example file and set your settings:

```bash
cp ./api/.env.example ./api/.env
```

Run migrations:

```bash
./api/manage.py migrate
```

Start building your awesome project!
