.ONESHELL:

check-migrations:
	python manage.py makemigrations --check --dry-run

check:
	black . --check \
	&& ruff check . \
	&& safety check \
	&& make check-migrations

check-fix:
	black .
	ruff check --fix-only --show-fixes --statistics .

