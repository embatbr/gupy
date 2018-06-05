#!/bin/bash


export SERVICE_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $SERVICE_ROOT_PATH


GUPY_ENV="$1"
if [ -z "$GUPY_ENV" ]; then
    GUPY_ENV="dev"
fi
export GUPY_ENV


if [ "$GUPY_ENV" == "dev" ];then
    db/actions.sh reset
    gunicorn --reload app.main
else
    gunicorn app.main
fi
