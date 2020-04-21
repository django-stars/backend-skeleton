import json
import os

from abc import ABC, abstractmethod
from urllib import request

from distutils import version as distutils_version
from packaging import version as packaging_version


class AbstractHook(ABC):  # pragma: no cover

    @abstractmethod
    def run(self):
        pass


class GenerateRequirementsInFileHook(AbstractHook):

    def __init__(self):
        self._project_requirements_with_versions_need_to_be_pinned = (
            "Celery",
            "Django",
            "django-environ",
            "django-filter",
            "djangorestframework",
            "djangorestframework-jwt",
            "drf-yasg",
            "gunicorn",
            "psycopg2-binary",
            "redis",
            "sentry-sdk",
        )
        self._project_requirements_with_versions_do_not_need_to_be_pinned = ("pytz", )
        self._dev_requirements_with_versions_need_to_be_pinned = (
            "Pygments",
            "Werkzeug",
            "bandit",
            "coverage",
            "django-debug-toolbar",
            "django-extensions",
            "docker-compose",
            "fabric",
            "invoke",
            "ipdb",
            "ipython",
            "isort",
            "model-bakery",
            "pip-tools",
            "pre-commit",
            "pylama",
            "pylint",
            "pylint-celery",
            "pylint-django",
            "pytest-bandit",
            "pytest-black",
            "pytest-cov",
            "pytest-django",
            "pytest-isort",
            "pytest-mock",
            "pytest",
            "radon",
            "safety",
        )
        self._dev_requirements_with_versions_do_not_need_to_be_pinned = ("black==19.3b0",)

    @staticmethod
    def _get_package_data(package):  # pragma: no cover
        return json.loads(request.urlopen(f"https://pypi.python.org/pypi/{package}/json").read().decode("utf-8"))

    def _get_latest_stable_version(self, package):
        data = self._get_package_data(package)
        version = max(
            [
                distutils_version.LooseVersion(release) for release in data["releases"]
                if not packaging_version.parse(release).is_prerelease
            ]
        )
        return f"{package}=={version}"

    def _get_project_packages(self):
        packages = list(
            map(self._get_latest_stable_version, self._project_requirements_with_versions_need_to_be_pinned)
        )
        packages.extend(self._project_requirements_with_versions_do_not_need_to_be_pinned)
        packages.sort()
        return packages

    def _get_dev_packages(self):
        packages = list(map(self._get_latest_stable_version, self._dev_requirements_with_versions_need_to_be_pinned))
        packages.extend(self._dev_requirements_with_versions_do_not_need_to_be_pinned)
        packages.sort()
        return packages

    def _render_requirements_build_file(self):
        print("Adding project requirements into requirements-build.in ...")
        content = []
        project_packages = self._get_project_packages()
        content.extend([f"{package}\n" for package in project_packages])
        return content

    def _render_requirements_dev_file(self):
        content = ["-r requirements-build.in\n\n"]
        print("Adding dev & test requirements into requirements-dev.in ...")
        dev_packages = self._get_dev_packages()
        content.extend([f"{package}\n" for package in dev_packages])
        return content

    @staticmethod
    def _write_requirements_build_file(content):
        path = os.path.join(os.getcwd(), "api", "requirements-build.in")
        with open(path, "w+") as f:
            f.writelines(content)

    @staticmethod
    def _write_requirements_dev_file(content):
        path = os.path.join(os.getcwd(), "api", "requirements-dev.in")
        with open(path, "w+") as f:
            f.writelines(content)

    def run(self):
        requirements_build_file_content = self._render_requirements_build_file()
        self._write_requirements_build_file(requirements_build_file_content)
        requirements_dev_file_content = self._render_requirements_dev_file()
        self._write_requirements_dev_file(requirements_dev_file_content)


class PostGenerateProjectFacade:

    def __init__(self):
        self._hook_1 = GenerateRequirementsInFileHook()

    def run(self):
        self._hook_1.run()


if __name__ == "__main__":  # pragma: no cover
    post_generate_project_facade = PostGenerateProjectFacade()
    post_generate_project_facade.run()
