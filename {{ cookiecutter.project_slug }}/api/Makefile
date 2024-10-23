.ONESHELL:

install:
	poetry install --with dev

lock:
	poetry lock

test:
	pytest --no-migrations

check-migrations:
	python manage.py makemigrations --check --dry-run

migrate:
	python manage.py migrate

collectstatic:
	python manage.py collectstatic --noinput

check:
	ruff format . --check \
	&& ruff check . \
	&& safety check --ignore=70612 \
	&& make check-migrations \

check-fix:
	ruff format .
	ruff check --fix-only --show-fixes --statistics .

run:migrate collectstatic
	python manage.py runserver_plus 0.0.0.0:8000 --nostatic

celery-worker-run:
	celery -A {{ cookiecutter.project_slug }} worker

celery-beat-run:
	celery -A {{ cookiecutter.project_slug }} beat
