# Use official slim Python base
FROM python:3.13.2-slim

# Install OS-level deps for psycopg and any build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Install Python deps (layer cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    # install Gunicorn for production
    && pip install --no-cache-dir gunicorn

# 2) Copy in project code
COPY . .

# 3) Make entrypoint executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Unbuffered logging
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
