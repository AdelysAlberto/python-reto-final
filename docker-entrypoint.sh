#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h db -p 5432 -U myuser; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"
echo "Running database migrations..."
python manage.py

echo "Starting application..."
exec "$@"