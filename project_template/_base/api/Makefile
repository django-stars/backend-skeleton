PROJECTNAME=$(notdir $(shell pwd))


run:
	python manage.py runserver_plus

test:
	pytest -s -l --verbose --strict --pylava ${PROJECTNAME}

migrate:
	python manage.py migrate

req-compile:
	@for fl in $(shell ls requirements/); do pip-compile requirements/$${fl}; done
