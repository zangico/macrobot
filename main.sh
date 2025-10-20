#!/bin/bash

APP_DIR="$(realpath "$(dirname "${BASH_SOURCE[0]}")")"

TEMP_DIR="$APP_DIR/.temp"
LOGS_DIR="$APP_DIR/logs"

PID_FILE="$TEMP_DIR/gunicorn.pid"
LOG_FILE="$LOGS_DIR/gunicorn.log"

export PYTHONPATH="$APP_DIR/src:$APP_DIR"

source ".venv/bin/activate" || exit 1

mkdir -p "$TEMP_DIR" "$LOGS_DIR"

ruff check . || { echo "Linting failed"; exit 1; }

MODE=${1:---prod}

set -a
source .env
set +a

export API__HOST=127.0.0.1

: "${APP__NAME:=orbita}"

if [ "$MODE" == "--dev" ]; then

    echo "🚀 Starting $APP__NAME in DEVELOPMENT mode..."
    python src/main.py
else
    echo "🚀 Starting $APP__NAME in PRODUCTION mode..."
    gunicorn src.main:app -c gunicorn_conf.py
fi


