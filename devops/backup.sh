#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

set -a
[ -f  $SCRIPT_DIR/.env ] && . $SCRIPT_DIR/.env && echo "Local environment variables loaded"
set +a

echo "Backuping $APP_NAME as `whoami`"

# Create the backup directory if it doesn't exist
test -d $BACKUP_DIR || mkdir -p $BACKUP_DIR

# Run the backups
DATE=`date '+%Y%m%d'`

echo "SQL dump"
pg_dump -U $DB_USER -h $DB_HOST -d $DB_NAME -W -F c -Z 9 -f $BACKUP_DIR/oc-db-$DATE.sql.gz

echo "media backup"
cd $DJANGO_DIR
tar cvzf $BACKUP_DIR/oc-media-$DATE.tar.gz media/

echo "New backup files:"
ls -hal $BACKUP_DIR/*$DATE*
