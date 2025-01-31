FROM python:{{ cookiecutter.python_version.lower()}}-slim AS base

ENV PYTHONUNBUFFERED 1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # to use `make` command
  make \
  # to install `poetry`
  curl

RUN pip install --no-cache -U pip setuptools \
    && rm -rf /root/.cache/pip \
    && curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/bin"

# `./api/poetry.lock` is optional to install dependency, see https://python-poetry.org/docs/basic-usage/#installing-without-poetrylock,
# so ./api/poetry.loc[k] is workaround do not fail when `./api/poetry.lock` does not exist.
COPY ./api/pyproject.toml ./api/poetry.loc[k] /opt/api/

WORKDIR /opt/api/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-cache --no-ansi --no-interaction --only main \
    && poetry cache clear pypi --all

COPY ./docker/images/api/files/entrypoint.sh /opt/docker/entrypoint.sh
RUN chmod +x /opt/docker/entrypoint.sh
ENTRYPOINT ["/opt/docker/entrypoint.sh"]


FROM base AS local

RUN poetry install --no-root --no-cache --no-ansi --no-interaction --with dev \
    && poetry cache clear pypi --all


FROM base AS live

COPY ./api /opt/api
