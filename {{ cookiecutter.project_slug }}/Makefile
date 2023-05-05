.ONESHELL:

api-test:
	cd api/ && make test

api-check-migrations:
	cd api/ && make check-migrations

api-check:
	cd api/ && make check

api-check-fix:
	cd api/ && make check-fix

api-poetry-install:
	cd api/ && make poetry-install

api-poetry-lock:
	cd api/ && make poetry-lock

api-run:
	cd api/ && make run

compose-up:
	cd docker/ && docker compose -f docker-compose-local.yml up

compose-down:
	cd docker/ && docker compose -f docker-compose-local.yml down
