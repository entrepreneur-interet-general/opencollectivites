#!/bin/bash

set -a
[ -f  .env ] && . .env
set +a

echo "Updating $NAME as `whoami`"

sudo service GUNICORN_SERVICE stop
# Go to the directory and update if needed
cd $DJANGODIR
git pull
git submodule update
$PIPENV install
$PIPENV run python manage.py migrate
$PIPENV run python manage.py collectstatic --no-input

sudo service GUNICORN_SERVICE start
