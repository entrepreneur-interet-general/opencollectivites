#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a
[ -f  $SCRIPT_DIR/.env ] && . $SCRIPT_DIR/.env && echo "Local environment variables loaded"
set +a

echo "Restarting $NAME as `whoami`"

sudo service $GUNICORN_SERVICE stop && echo "Service $GUNICORN_SERVICE stopped"

sudo service $GUNICORN_SERVICE start && echo "Service $GUNICORN_SERVICE started"
sudo service $GUNICORN_SERVICE status
