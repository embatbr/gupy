#!/bin/bash


export PROJECT_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $PROJECT_ROOT_PATH


ACTION="$1"


if [ "$ACTION" == "create" ]; then
    echo "Creating user and database locally."

    createuser --connection-limit=50 gupy;
    createdb --owner=gupy gupy;

    read -s -p "Type new password: " PASSWORD
    echo
    psql -c "ALTER USER gupy PASSWORD '$PASSWORD';"

elif [ "$ACTION" == "drop" ]; then
    echo "Dropping user and database locally."

    dropdb gupy
    dropuser gupy

elif [[ "up down"[*] =~ $ACTION ]]; then
    echo "Running action '$ACTION'."

    read -s -p "Type password for user 'gupy': " PASSWORD
    echo
    echo "Loading file '$ACTION.sql'"
    PGPASSWORD=$PASSWORD psql -h localhost -p 5432 -U gupy -d gupy -f $ACTION.sql

elif [[ $ACTION == "reset" ]]; then
    echo "Running action '$ACTION'."

    read -s -p "Type password for user 'gupy': " PASSWORD
    echo
    PGPASSWORD=$PASSWORD psql -h localhost -p 5432 -U gupy -d gupy -f down.sql
    PGPASSWORD=$PASSWORD psql -h localhost -p 5432 -U gupy -d gupy -f up.sql

elif [ "$ACTION" == "access" ]; then
    echo "Accessing database."

    read -s -p "Type password for user 'gupy': " PASSWORD
    echo
    echo "Accessing database 'gupy'."
    PGPASSWORD=$PASSWORD psql -h localhost -p 5432 -U gupy -d gupy

fi
