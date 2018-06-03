#!/bin/bash


export SERVICE_ROOT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd $SERVICE_ROOT_PATH


ENV="$1"
if [ -z "$ENV" ]; then
    ENV="dev"
fi


if [ "$ENV" == "dev" ];then
    gunicorn --reload app.main
else
    gunicorn app.main
fi
