# Django Stars Backend Skeleton

Basically django template for project creation that don't need django to start a project.

## How to use

  1. open terminal
  1. copy ```curl http://be.skeletons.djangostars.com/startproject | sh```
  1. paste
  1. hit enter

This command will ask you about needed python version, name of project and template and create project skeleton

## Template features

### Base teamplate

  * **Django** project formatted according to Django Stars Code Style requirements
  * **django-environ** to keep all configuration in environment
  * **psycopg2** as default database driver
  * **django-extensions/ipython/ipdb** for debug purposes
  * **pytest** with **pylava** for testing

### Django REST Framework

add [DRF](http://django-rest-framework.org) to base template

### Celery

add [Celery](http://www.celeryproject.org/) to base template
