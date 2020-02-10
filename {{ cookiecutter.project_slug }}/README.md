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

Install Python {{ cookiecutter.python_version }} & setup virtual environment. We recommend to use [pyenv](https://github.com/pyenv/pyenv) & [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv):

```bash
pyenv install {{ cookiecutter.python_version }}
pyenv virtualenv {{ cookiecutter.python_version }} {{ cookiecutter.project_slug }}
pyenv activate {{ cookiecutter.project_slug }}
```

Update `pip` & `setuptools`, install `fabric`, `invoke` & `pip-tools`:

```bash
pip install -U fabric invoke pip pip-tools setuptools
```

Install Python requirements:

```bash
fab pip.sync
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
{{ cookiecutter.project_slug | upper() }}_SECRET_KEY=<your-generated-key>
```

Run backing services (require Docker):

```bash
fab compose.up -d
```

Run migrations:

```bash
./api/manage.py migrate
```

Run Django server:

```bash
fab run
```
