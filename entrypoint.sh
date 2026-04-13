#!/bin/sh
set -e

# Seed questions on first run (safe to re-run — skips if DB already has data)
python -m backend.seed.seed_questions

# Start server (no --reload in production)
exec python -m uvicorn backend.main:app \
  --host 0.0.0.0 \
  --port 8000
