PROJECTNAME=$(notdir $(shell pwd))


run:
	pipenv run python -x manage.py runserver_plus

test:
	pipenv run pytest -s -l --verbose --strict --pylava ${PROJECTNAME}

migrate:
	pipenv run python manage.py migrate
