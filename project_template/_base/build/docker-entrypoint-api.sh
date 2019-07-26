#!/bin/sh

cd /api/

python manage.py migrate

exec "$@"