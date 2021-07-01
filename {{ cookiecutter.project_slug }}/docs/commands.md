# {{ cookiecutter.project_name }}: Management commands (fabric/invoke) #

We use [fabric](http://docs.fabfile.org/en/latest/) and [invoke](http://www.pyinvoke.org/) to automate routine tasks like deployment, builds, making backups, etc.

## Commands for backend ##

Run backend locally:

```bash
fab run
```

Run `shell_plus`:

```bash
fab shell
```

Run Celery worker & beat locally:

```bash
fab celery.all
```

Run Celery worker only locally:

```bash
fab celery.worker
```

Run Celery beat only locally:

```bash
fab celery.beat
```

Clear Celery queue:

```bash
fab celery.clear
```

Clean *.pyc files:

```bash
fab clean-pyc
```

Run tests:

```bash
fab test
```

Check Python formatting with [black](https://black.readthedocs.io/en/stable/):

```bash
fab test.black
```

Fix Python formatting with black:

```bash
fab test.black-apply
```

Check imports order with [isort](https://isort.readthedocs.io/en/latest/):

```bash
fab test.isort
```

Fix imports order with isort:

```bash
fab test.isort-apply
```

Test security issues with [bandit](https://bandit.readthedocs.io/en/latest/):

```bash
fab test.bandit
```

Run different checks ([pycodestyle](https://pypi.org/project/pycodestyle/), [pyflakes](https://pypi.org/project/pyflakes/), [mccabe](https://pypi.org/project/mccabe/), [radon](https://pypi.org/project/radon/)) with [pylama](https://pypi.org/project/pylama/):

```bash
fab test.pylama
```

Check Python code with [pylint](https://www.pylint.org/):

```bash
fab test.pylint
```

Check Python dependencies for know vulnerabilities with [safety](https://pyup.io/safety/):

```bash
fab test.safety
```

Run tests + all linters described above:

```bash
fab test.all
```

## Frontend ##

Build frontend locally (`yarn build`):

```bash
fab fe.build
```

Run frontend locally (`yarn start`)

```bash
fab fe.start
```

## Run 3rd party: ##

Run PostgreSQL, Redis and [Mailhog](https://github.com/mailhog/MailHog) (for testing emails) locally in Docker:

```bash
fab compose.up
```

Run in background:

```bash
fab compose.up -d
```

Stop 3rd-party services:

```bash
fab compose.down
```

Stop 3rd-party services and delete their data:

```bash
fab compose.down -v
```

## Delete merged GIT-branches ##

This command will locally remove all currently merged GIT branches except `develop`, `stage` and `production`.

```bash
fab git.delete-stale
```

Get Github pull request [as a local branch](https://help.github.com/en/articles/checking-out-pull-requests-locally):

```
fab git.checkout-pr <pr-number>
```

## Update python requirements with pip-tools ##

To work with a list of Python requirements we use [pip-tools](https://github.com/jazzband/pip-tools) utility.

To compile all requirement files run this command:

```bash
fab pip.compile
```

To synchronize requirements run this command:

```bash
fab pip.sync
```
