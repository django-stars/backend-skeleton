.ONESHELL:

install:
	poetry install --with dev --no-root

lock:
	poetry lock

poetry-shell:
	poetry shell

test:
	poetry run pytest --no-migrations

check-migrations:
	poetry run python manage.py makemigrations --check --dry-run

migrate:
	poetry run python manage.py migrate

check:
	poetry run black . --check
	poetry run ruff check .
	poetry run safety check
	poetry run make check-migrations

check-fix:
	poetry run black .
	poetry run ruff check --fix-only --show-fixes --statistics .

run:migrate
	poetry run python manage.py runserver_plus 0.0.0.0:8000

