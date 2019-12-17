from hooks.post_gen_project import GenerateRequirementsInFileHook


def test_get_project_packages(mocker):
    hook = GenerateRequirementsInFileHook()
    mocked_get_latest_stable_version = lambda x: f"{x}==<mocked>"
    mocker.patch.object(hook, "_get_latest_stable_version", mocked_get_latest_stable_version)

    packages = hook._get_project_packages()

    assert packages == [
        "Celery==<mocked>",
        "Django==<mocked>",
        "django-environ==<mocked>",
        "django-filter==<mocked>",
        "djangorestframework-jwt==<mocked>",
        "djangorestframework==<mocked>",
        "drf-yasg==<mocked>",
        "gunicorn==<mocked>",
        "psycopg2-binary==<mocked>",
        "pytz",
        "redis==<mocked>",
        "sentry-sdk==<mocked>",
    ]


def test_get_dev_packages(mocker):
    hook = GenerateRequirementsInFileHook()
    mocked_get_latest_stable_version = lambda x: f"{x}==<mocked>"
    mocker.patch.object(hook, "_get_latest_stable_version", mocked_get_latest_stable_version)

    packages = hook._get_dev_packages()

    assert packages == [
        "Pygments==<mocked>",
        "Werkzeug==<mocked>",
        "bandit==<mocked>",
        "black==19.3b0",
        "coverage==<mocked>",
        "django-debug-toolbar==<mocked>",
        "django-extensions==<mocked>",
        "docker-compose==<mocked>",
        "fabric==<mocked>",
        "invoke==<mocked>",
        "ipdb==<mocked>",
        "ipython==<mocked>",
        "isort==<mocked>",
        "model-bakery==<mocked>",
        "pip-tools==<mocked>",
        "pre-commit==<mocked>",
        "pylama==<mocked>",
        "pylint-celery==<mocked>",
        "pylint-django==<mocked>",
        "pylint==<mocked>",
        "pytest-bandit==<mocked>",
        "pytest-black==<mocked>",
        "pytest-cov==<mocked>",
        "pytest-django==<mocked>",
        "pytest-isort==<mocked>",
        "pytest-mock==<mocked>",
        "pytest==<mocked>",
        "radon==<mocked>",
        "safety==<mocked>",
    ]


def test_render_requirements_file(mocker):
    hook = GenerateRequirementsInFileHook()
    project_packages_mock = ["project-package-1=<mocked>", "project-package-2=<mocked>"]
    dev_packages_mock = ["dev-package-1=<mocked>", "dev-package-2=<mocked>"]
    mocker.patch.object(hook, "_get_project_packages", return_value=project_packages_mock)
    mocker.patch.object(hook, "_get_dev_packages", return_value=dev_packages_mock)

    content = hook._render_requirements_file()

    assert content == [
        "# Project requirements\n\n",
        "project-package-1=<mocked>\n",
        "project-package-2=<mocked>\n",
        "\n\n",
        "# Dev & test requirements\n\n",
        "dev-package-1=<mocked>\n",
        "dev-package-2=<mocked>\n",
    ]


def test_run(mocker):
    hook = GenerateRequirementsInFileHook()
    mocker.patch("os.getcwd", return_value="/path/to/project")
    mocker.patch.object(hook, "_render_requirements_file", return_value=["requirements_file_mocked_content"])
    open_mock = mocker.patch('builtins.open', mocker.mock_open())

    hook.run()

    open_mock.assert_called_once_with("/path/to/project/api/requirements.in", "w+")
    handle_open_mock = open_mock()
    handle_open_mock.writelines.assert_called_once_with(["requirements_file_mocked_content"])
