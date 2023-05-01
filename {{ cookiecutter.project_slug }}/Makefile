.ONESHELL:

api-test:
	cd api/ && make test

api-check-migrations:
	cd api/ && make check-migrations

api-check:
	cd api/ && make check

api-check-fix:
	cd api/ && make check-fix

api-pip-compile:
	cd api/ && make pip-compile

api-pip-sync:
	cd api/ && make pip-sync

compose-up:
	cd docker/ &&docker-compose --file docker-compose-local.yml up

compose-down:
	cd docker/ &&docker-compose --file docker-compose-local.yml down
