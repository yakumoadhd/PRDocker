#!/bin/sh
export PATH="/usr/local/searxng/.venv/bin:$PATH"
export SEARXNG_PORT=8080
export GRANIAN_PORT=8080
export SEARXNG_SETTINGS_PATH=/etc/searxng/settings.yml

/usr/local/searxng/.venv/bin/granian \
    --host 127.0.0.1 \
    --port 8080 \
    searx.webapp:app &

sleep 5

exec /usr/bin/python3.14 -m uvicorn proxy:app --host 0.0.0.0 --port 7860 --app-dir /
