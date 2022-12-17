pip-compile:
	pip-compile pyproject.toml \
		--generate-hashes --upgrade --output-file requirements.txt --resolver=backtracking
	pip-compile pyproject.toml \
		--generate-hashes --upgrade --extra dev --output-file requirements-dev.txt --resolver=backtracking

pip-sync: pip-compile
	pip-sync requirements.txt

pip-sync-dev: pip-compile
	pip-sync requirements-dev.txt

black-check:
	black {{ cookiecutter.project_slug }} --check

isort-check:
	isort {{ cookiecutter.project_slug }} --check

pylama-check:
	pylama

bandit-check:
	bandit -c pyproject.toml -r .

safety-check:
	safety check

migrations-check:
	python manage.py makemigrations --check --dry-run

reformat-code:
	isort {{ cookiecutter.project_slug }}
	black {{ cookiecutter.project_slug }}
