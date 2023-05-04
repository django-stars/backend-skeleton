.ONESHELL:

test:
	pytest --no-migrations

check-migrations:
	python manage.py makemigrations --check --dry-run

check:
	black . --check
	ruff check .
	safety check
	make check-migrations

check-fix:
	black .
	ruff check --fix-only --show-fixes --statistics .

pip-compile:
	pip-compile --upgrade --allow-unsafe --generate-hashes -o ./requirements-build.txt ./requirements-build.in
	pip-compile --upgrade --allow-unsafe --generate-hashes -o ./requirements-dev.txt ./requirements-dev.in

pip-sync:
	pip-sync ./requirements-dev.txt

run:
	@python manage.py runserver_plus 0.0.0.0:8000
