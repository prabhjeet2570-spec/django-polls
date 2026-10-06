#!/usr/bin/env bash
set -euo pipefail
cd /var/app/staging
PYTHON=$(find /var/app/venv -path '*/bin/python' -print -quit)
install -d -o webapp -g webapp -m 0750 /var/app/data
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py seed_polls
"$PYTHON" manage.py collectstatic --noinput
chown webapp:webapp /var/app/data/db.sqlite3
chmod 0640 /var/app/data/db.sqlite3
