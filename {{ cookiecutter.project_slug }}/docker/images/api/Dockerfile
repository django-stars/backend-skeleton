FROM python:{{ cookiecutter.python_version.lower()}}-slim AS base

ENV PYTHONUNBUFFERED 1 \
    UV_COMPILE_BYTECODE 1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # dependencies for healthcheck
  curl \
  # to use `make` command
  make

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV PATH="${PATH}:/root/.local/bin"

COPY ./api/pyproject.toml ./api/uv.lock /opt/api/

WORKDIR /opt/api/

RUN uv export --frozen --format requirements-txt | uv pip install --system -r /dev/stdin && \
    uv cache clean

COPY ./docker/images/api/files/entrypoint.sh /opt/docker/entrypoint.sh
RUN chmod +x /opt/docker/entrypoint.sh
ENTRYPOINT ["/opt/docker/entrypoint.sh"]


FROM base AS local

EXPOSE 8000


FROM base AS live

COPY ./api /opt/api

EXPOSE 8000
