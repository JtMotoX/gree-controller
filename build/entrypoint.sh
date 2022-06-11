#!/bin/sh

set -e

cd "$(dirname "$0")"

if [ "$1" = "run" ]; then
	gunicorn --bind 0.0.0.0:5001 --reload gree.wsgi:app
	exit 1
fi

exec "$@"
