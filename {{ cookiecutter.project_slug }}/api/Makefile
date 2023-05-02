.ONESHELL:

test:
	pytest --no-migrations

check-migrations:
	python manage.py makemigrations --check --dry-run

check:
	black . --check
	isort . --check
	pylint {{ cookiecutter.project_slug }}
	bandit -r . -c pyproject.toml
	pylama .
	safety check
	make check-migrations

check-fix:
	black .
	isort .

pip-compile:
	pip-compile --upgrade --allow-unsafe --generate-hashes -o ./requirements-build.txt ./requirements-build.in
	pip-compile --upgrade --allow-unsafe --generate-hashes -o ./requirements-dev.txt ./requirements-dev.in

pip-sync:
	pip-sync ./requirements-dev.txt
