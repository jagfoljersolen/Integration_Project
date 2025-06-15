# ───────────────────────────────
# 1) BUILDER STAGE
# ───────────────────────────────
FROM python:3.13.2-slim AS builder

# Install compilers & headers for building wheels
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /install

# Copy and install Python deps into /install
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt \
 && pip install --no-cache-dir --prefix=/install gunicorn

# ───────────────────────────────
# 2) RUNTIME STAGE
# ───────────────────────────────
FROM python:3.13.2-slim

WORKDIR /app

# 2a) Copy pure Python environment (all site-packages, scripts, etc.)
COPY --from=builder /install /usr/local

# 2b) Copy application code
COPY . .

# 2c) Entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Ensure Python output is unbuffered (for live logs)
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["./entrypoint.sh"]
