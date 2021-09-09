#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a
[ -f  $SCRIPT_DIR/.env ] && . $SCRIPT_DIR/.env && echo "Local environment variables loaded"
set +a

echo "Updating $NAME as `whoami`"

sudo service $GUNICORN_SERVICE stop && echo "Service $GUNICORN_SERVICE stopped"

# Go to the directory and update if needed
cd $DJANGO_DIR
git pull
git submodule update
$POETRY install
$POETRY run python manage.py migrate
$POETRY run python manage.py collectstatic --no-input

sudo service $GUNICORN_SERVICE start && echo "Service $GUNICORN_SERVICE started"
sudo service $GUNICORN_SERVICE status
