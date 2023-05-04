FROM python:{{ cookiecutter.python_version.lower()}}-slim as base

ARG DOCKER_USER_ID=1000
ARG DOCKER_GROUP_ID=1000

ENV PYTHONUNBUFFERED 1

RUN groupadd -g ${DOCKER_GROUP_ID} user \
    && useradd --shell /bin/bash -u $DOCKER_USER_ID -g $DOCKER_GROUP_ID -o -c "" -m user

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev

RUN pip install --no-cache -U pip setuptools pip-tools \
    && rm -rf /root/.cache/pip

COPY --chown=user:user ./api/requirements-build.txt /opt/api/requirements-build.txt

WORKDIR /opt/api/

RUN pip install --no-cache -r requirements-build.txt \
    && rm -rf /root/.cache/pip


COPY --chown=user:user ./docker/images/api/files/docker-entrypoint.sh /opt/docker/docker-entrypoint.sh
RUN chmod +x /opt/docker/docker-entrypoint.sh


COPY --chown=user:user ./api /opt/api

ENTRYPOINT ["/opt/docker/entrypoint.sh"]

USER user


FROM base as local

USER root

COPY --chown=user:user ./api/requirements-dev.txt /opt/api/requirements-dev.txt

RUN pip install --no-cache -r requirements-dev.txt \
    && rm -rf /root/.cache/pip
