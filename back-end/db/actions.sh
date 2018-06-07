#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $PROJECT_ROOT_PATH


ACTION="$1"
PASSWORD_MASTER="gupy_master"
PASSWORD_WRITER="gupy_writer"
PASSWORD_READER="gupy_reader"


if [ "$ACTION" == "create" ]; then
    echo "Creating user and database locally."

    createuser --connection-limit=1 gupy_master;
    createuser --connection-limit=1 gupy_writer; # permission to only insert data into some tables
    createuser --connection-limit=1 gupy_reader; # permission to only select data from some tables
    createdb --owner=gupy_master gupy;

    if [ "$GUPY_ENV" != "dev" ];then
        read -s -p "Type new password (gupy_master): " PASSWORD_MASTER
        read -s -p "Type new password (gupy_writer): " PASSWORD_WRITER
        read -s -p "Type new password (gupy_reader): " PASSWORD_READER
    fi
    echo

    psql -c "ALTER USER gupy_master PASSWORD '$PASSWORD_MASTER';"
    psql -c "ALTER USER gupy_writer PASSWORD '$PASSWORD_WRITER';"
    psql -c "ALTER USER gupy_reader PASSWORD '$PASSWORD_READER';"

elif [ "$ACTION" == "drop" ]; then
    echo "Dropping user and database locally."

    dropdb gupy
    dropuser gupy_master
    dropuser gupy_writer
    dropuser gupy_reader

elif [[ "up down"[*] =~ $ACTION ]]; then
    echo "Running action '$ACTION'."

    if [ "$GUPY_ENV" != "dev" ];then
        read -s -p "Type password for user 'gupy_master': " PASSWORD_MASTER
    fi
    echo
    echo "Loading file '$ACTION.sql'"
    PGPASSWORD=$PASSWORD_MASTER psql -h localhost -p 5432 -U gupy_master -d gupy -f $ACTION.sql

elif [[ $ACTION == "reset" ]]; then
    echo "Running action '$ACTION'."

    if [ "$GUPY_ENV" != "dev" ];then
        read -s -p "Type password for user 'gupy_master': " PASSWORD_MASTER
    fi
    echo
    PGPASSWORD=$PASSWORD_MASTER psql -h localhost -p 5432 -U gupy_master -d gupy -f down.sql
    PGPASSWORD=$PASSWORD_MASTER psql -h localhost -p 5432 -U gupy_master -d gupy -f up.sql

elif [ "$ACTION" == "access" ]; then
    echo "Accessing database."

    if [ "$GUPY_ENV" != "dev" ];then
        read -s -p "Type password for user 'gupy_reader': " PASSWORD_READER
    fi
    echo
    echo "Accessing database 'gupy'."
    PGPASSWORD=$PASSWORD_READER psql -h localhost -p 5432 -U gupy_reader -d gupy

fi
