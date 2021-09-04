import os


__all__ = [
    "project_path",
    "print_success",
    "print_error",
    "print_warning",
    "fail",
    "config",
]


_PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)


def project_path(*args):
    return os.path.join(_PROJECT_PATH, *args)


def color_print(message: str, color: str) -> None:
    print(f"{color}{message}\x1b[0m")


def print_success(message: str) -> None:
    color_print(message, "\x1b[32m")


def print_error(message: str) -> None:
    color_print(message, "\x1b[31m")


def print_warning(message: str) -> None:
    color_print(message, "\x1b[33m")


def fail(message: str) -> None:
    print_error(message)
    exit(1)


_PROJECT_NAME = "{{ cookiecutter.project_slug }}"
_AVAILABLE_ENVIRONMENTS = (
    "develop",
    "beta",
    "production",
)

config = {
    "project_name": _PROJECT_NAME,
    "available_environments": _AVAILABLE_ENVIRONMENTS,
}
