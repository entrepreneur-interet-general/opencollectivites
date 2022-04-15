#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a
[ -f  $SCRIPT_DIR/.env ] && . $SCRIPT_DIR/.env && echo "Local environment variables loaded"
set +a

echo "Stopping $NAME as `whoami`"

sudo service $GUNICORN_SERVICE stop && echo "Service $GUNICORN_SERVICE stopped"
