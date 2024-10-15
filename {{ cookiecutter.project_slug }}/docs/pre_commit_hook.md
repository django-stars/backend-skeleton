# {{ cookiecutter.project_name }}: Pre-commit hooks #

To run additional checks before making commit we use [Pre-commit](https://pre-commit.com/) hooks.


Since the `api` is running inside docker container we don't have a pre-commit as a dependency there, so you need to 
install `pre-commit` package [manually](https://pre-commit.com/#install).

> [!NOTE]  
> The `safety` hook also [requires](https://github.com/Lucas-C/pre-commit-hooks-safety?tab=readme-ov-file#supported-files) `poetry` to be in your `PATH`.
> Ensure the poetry [installed](https://python-poetry.org/docs/#installation) with the same python version as in `pyproject.toml`

You need to generate the actual git pre-commit hook. It should be done only once:

```bash
pre-commit install --install-hooks
```

To run pre-commit hooks manually:

```bash
pre-commit run --all-files
```

To run specific hook:

```
pre-commit run <hook_id>
```

See more info in official documentation:

* [Usage](https://pre-commit.com/#usage)
* [Adding new hooks](https://pre-commit.com/#plugins)
