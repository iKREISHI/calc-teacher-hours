#!/bin/bash

cd /app
export DJANGO_SETTINGS_MODULE=config.settings
echo "Применение миграций Django..."
uv run python3 manage.py collectstatic --noinput --clear
uv run python3 manage.py makemigrations user schedule calculation
uv run python3 manage.py migrate
# uv run python3 manage.py temp_import

exec "$@"