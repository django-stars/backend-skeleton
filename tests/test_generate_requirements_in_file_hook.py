from hooks.post_gen_project import GenerateRequirementsInFileHook


def test_get_project_packages(mocker):
    hook = GenerateRequirementsInFileHook()
    mocked_get_latest_stable_version = lambda x: f"{x}==<mocked>"
    mocker.patch.object(
        hook, "_get_latest_stable_version", mocked_get_latest_stable_version
    )

    packages = hook._get_project_packages()

    assert packages == [
        "Celery==<mocked>",
        "Django==<mocked>",
        "django-environ==<mocked>",
        "django-filter==<mocked>",
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
    mocker.patch.object(
        hook, "_get_latest_stable_version", mocked_get_latest_stable_version
    )

    packages = hook._get_dev_packages()

    assert packages == [
        "Pygments==<mocked>",
        "Werkzeug==<mocked>",
        "bandit==<mocked>",
        "black==21.6b0",
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
        "pytest-cov==<mocked>",
        "pytest-django==<mocked>",
        "pytest-mock==<mocked>",
        "pytest==<mocked>",
        "radon==<mocked>",
        "safety==<mocked>",
    ]


def test_render_requirements_build_file(mocker):
    hook = GenerateRequirementsInFileHook()
    project_packages_mock = ["project-package-1=<mocked>", "project-package-2=<mocked>"]
    mocker.patch.object(
        hook, "_get_project_packages", return_value=project_packages_mock
    )

    content = hook._render_requirements_build_file()

    assert content == [
        "project-package-1=<mocked>\n",
        "project-package-2=<mocked>\n",
    ]


def test_render_requirements_dev_file(mocker):
    hook = GenerateRequirementsInFileHook()
    dev_packages_mock = ["dev-package-1=<mocked>", "dev-package-2=<mocked>"]
    mocker.patch.object(hook, "_get_dev_packages", return_value=dev_packages_mock)

    content = hook._render_requirements_dev_file()

    assert content == [
        "-r requirements-build.in\n\n",
        "dev-package-1=<mocked>\n",
        "dev-package-2=<mocked>\n",
    ]


def test_write_requirements_build_file(mocker):
    hook = GenerateRequirementsInFileHook()
    mocker.patch("os.getcwd", return_value="/path/to/project")
    open_mock = mocker.patch("builtins.open", mocker.mock_open())

    hook._write_requirements_build_file(["mocked", "content"])

    open_mock.assert_called_once_with(
        "/path/to/project/api/requirements-build.in", "w+"
    )
    handle_open_mock = open_mock()
    handle_open_mock.writelines.assert_called_once_with(["mocked", "content"])


def test_write_requirements_dev_file(mocker):
    hook = GenerateRequirementsInFileHook()
    mocker.patch("os.getcwd", return_value="/path/to/project")
    open_mock = mocker.patch("builtins.open", mocker.mock_open())

    hook._write_requirements_dev_file(["mocked", "content"])

    open_mock.assert_called_once_with("/path/to/project/api/requirements-dev.in", "w+")
    handle_open_mock = open_mock()
    handle_open_mock.writelines.assert_called_once_with(["mocked", "content"])


def test_run(mocker):
    hook = GenerateRequirementsInFileHook()
    mocker.patch("os.getcwd", return_value="/path/to/project")
    mocked_render_requirements_build_file = mocker.patch.object(
        hook, "_render_requirements_build_file", return_value=["build", "content"]
    )
    mocked_render_requirements_dev_file = mocker.patch.object(
        hook, "_render_requirements_dev_file", return_value=["dev", "content"]
    )
    mocked_write_requirements_build_file = mocker.patch.object(
        hook, "_write_requirements_build_file"
    )
    mocked_write_requirements_dev_file = mocker.patch.object(
        hook, "_write_requirements_dev_file"
    )

    hook.run()

    mocked_render_requirements_build_file.assert_called_once()
    mocked_write_requirements_build_file.assert_called_once_with(["build", "content"])
    mocked_render_requirements_dev_file.assert_called_once()
    mocked_write_requirements_dev_file.assert_called_once_with(["dev", "content"])
