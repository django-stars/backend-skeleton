# {{ cookiecutter.project_name }}

[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://docs.astral.sh/ruff/formatter/)

### List of services: ###

* Dev server: [https://{{ cookiecutter.domain_name }}/](https://{{ cookiecutter.domain_name }}/)

### Documentation: ###

* [Architecture overview](docs/architecture_overview.md)
* [Backend: Routine tasks](docs/commands.md)
* [Backend: Pre-commit hook](docs/pre_commit_hook.md)
* [Backend: Docker configuration](docs/docker.md)

### API documentation: ###

* ReDoc web UI: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/redoc/](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/redoc/)
* Swagger web UI: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger/](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger/)
* Schema YAML: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/schema/](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/schema/)

### First run: ###
Application is running in docker containers. 

### Prerequisites
Installed [docker](https://docs.docker.com/engine/install/)

Copy initial settings for Django project:

```bash
cp ./api/.env.example ./api/.env
```

Run application with required services:

```bash
make compose-up
```

Your application will be available at [http://localhost:8000](http://localhost:8000)

How it works:
 - `make compose-up` will run docker-compose with (all services)[docker/docker.md]
   - if images is missed it will build them
   - if there is no `poetry.lock` file present, Poetry simply resolves all dependencies listed in your 
     `api/pyproject.toml` file and downloads the latest version of their files. 
     But in any case it's good practice to lock your dependencies and share the lock file with your team, 
     to do that run `make poetry-lock` command, and commit `poetry.lock` file to the repository.
 - it will use `api/.env` file to set environment variables for `api` and `celery` services. Check `env_file` section in [docker-compose.yml](docker/docker-compose.yml)

Any changes in docker files or python dependency will require to rebuild images, to do that run `make compose-build` command.

### Docker
Application is running in docker containers. It allows to run application in the same environment on any machine with 
minimal setup. 
If you need python environment, to run some commands, just use `make api-bash`, and you will be in the container with
all dependencies installed.

