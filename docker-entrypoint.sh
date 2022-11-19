#!/bin/sh
set -e
exec gunicorn --preload -c gunicorn.config.py "auth_service.app:create_app()"
