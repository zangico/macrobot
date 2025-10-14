#!/bin/bash

APP_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_DIR="$APP_DIR/.venv"
TEMP_DIR="$APP_DIR/.temp"
LOGS_DIR="$APP_DIR/logs"

PID_FILE="$TEMP_DIR/gunicorn.pid"
LOG_FILE="$LOGS_DIR/gunicorn.log"

export PYTHONPATH="$APP_DIR/src:$APP_DIR"


if ! source "$VENV_DIR/bin/activate"; then
    exit 1
fi

mkdir -p "$TEMP_DIR" "$LOGS_DIR"

ruff check . || { echo "Linting failed"; exit 1; }

if [[ "$1" == "-s" || "$1" == "--script" ]]; then
    if [[ -n "$2" ]]; then
    if [[ ! -f "scripts/$2.py" ]]; then
        echo "Script scripts/$2.py does not exist."
        exit 1
    fi
        echo "Running script: $2"
        python scripts/$2.py
        exit 0
    else
        echo "Usage: $0 [-s | --script] <script>"
        exit 1
    fi
fi

if [[ "$1" == "--dev" ]]; then
    uvicorn src.app:app --reload --no-access-log --host localhost --port 60010
else
    gunicorn src.app:app -k uvicorn.workers.UvicornWorker \
        -c "$APP_DIR/gunicorn_conf.py" \
        $( [[ "$1" == "-d" ]] && echo "--daemon" )
fi