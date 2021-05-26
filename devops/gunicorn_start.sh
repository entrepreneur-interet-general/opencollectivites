#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a
[ -f  $SCRIPT_DIR/.env ] && . $SCRIPT_DIR/.env && echo "Local environment variables loaded"
set +a

echo "Starting $NAME as `whoami`"

# Create the run directory if it doesn't exist
RUN_DIR=$(dirname $SOCKFILE)
test -d $RUN_DIR || mkdir -p $RUN_DIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
cd $DJANGO_DIR
exec $PIPENV run gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user $USER \
  --bind=unix:$SOCKFILE
