.ONESHELL:

api-bash:
	cd docker/ && docker compose run --rm api bash

api-test:
	cd docker/ && docker compose run --rm api make test

api-check-migrations:
	cd docker/ && docker compose run --rm api make check-migrations

api-check:
	cd docker/ && docker compose run --rm api make check

api-check-fix:
	cd docker/ && docker compose run --rm api make check-fix

api-lock:
	cd docker/ && docker compose run --rm api make lock

compose-up:
	cd docker/ && docker compose up

compose-down:
	cd docker/ && docker compose down

compose-build:
	cd docker/ && docker compose build
