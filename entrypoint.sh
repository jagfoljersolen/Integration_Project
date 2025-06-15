#!/usr/bin/env sh
set -e

# 1) Wait for Postgres via Python
echo "⏳ Waiting for Postgres..."
python - <<'EOF'
import os, time, psycopg
conn_info = dict(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST", "db"),
    port=os.getenv("DATABASE_PORT", "5432"),
)
while True:
    try:
        psycopg.connect(**conn_info).close()
        break
    except Exception:
        time.sleep(1)
EOF

# 2) cd into project
cd /app/integration_project

# 3) Migrations & imports
echo "🛠️  Applying migrations..."
python manage.py migrate --noinput

echo "📥 Importing CSVs..."
python manage.py import_commodity_with_units ./data/commodity_with_units.csv
python manage.py import_conflicts ./data/conflicts.csv --batch-size 1000

# 4) Start Gunicorn
echo "🚀 Starting Gunicorn..."
exec gunicorn integration_project.wsgi:application \
     --bind 0.0.0.0:8000 \
     --workers 3
