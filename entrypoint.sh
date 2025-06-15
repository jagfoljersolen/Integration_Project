#!/usr/bin/env sh
set -e

# 1) Wait for PostgreSQL to be ready
until pg_isready -h "${DATABASE_HOST:-db}" -p "${DATABASE_PORT:-5432}"; do
  echo "⏳ Waiting for Postgres..."
  sleep 1
done

# 1.1) Switch into the Django project dir where manage.py lives
cd integration_project

# 2) Run migrations
echo "🛠️  Applying migrations..."
python manage.py migrate --noinput

# 3) Load your CSV data
echo "📥 Importing commodity_with_units..."
python manage.py import_commodity_with_units data/commodity_with_units.csv

echo "📥 Importing conflicts..."
python manage.py import_conflicts data/conflicts.csv --batch-size 1000

# 4) Launch Gunicorn in 3 workers, binding all interfaces
echo "🚀 Starting Gunicorn..."
exec gunicorn integration_project.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3
