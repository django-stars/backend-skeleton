# {{ cookiecutter.project_name }}

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### List of services: ###

* Dev server: [https://{{ cookiecutter.domain_name }}/](https://{{ cookiecutter.domain_name }}/)

### Documentation: ###

* [Architecture overview](docs/architecture_overview.md)
* [Backend: Routine tasks](docs/commands.md)
* [Backend: Pre-commit hook](docs/pre_commit_hook.md)

### API documentation: ###

* ReDoc web UI: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/redoc/](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/redoc/)
* Swagger web UI: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger/](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger/)
* Swagger JSON: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger.json](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger.json)
* Swagger YAML: [https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger.yaml](https://{{ cookiecutter.domain_name }}/_platform/docs/v1/swagger.yaml)

### First run: ###

### Prerequisites
Installed [poetry](https://python-poetry.org/docs/#installation) and [docker](https://docs.docker.com/engine/install/)

Install python dependencies with poetry:

```bash
make api-poetry-install
```

Copy initial settings for Django project:

```bash
cp ./api/.env.example ./api/.env
```

Generate `SECRET_KEY`:

```bash
./api/manage.py generate_secret_key
```

and write it to `./api/.env`:

```
{{ cookiecutter.env_prefix }}SECRET_KEY=<your-generated-key>
```

Run backing services (require Docker):

```bash
make compose-up
```

Run Django server:

```bash
make api-run
```

