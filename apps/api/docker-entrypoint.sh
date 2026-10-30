#!/bin/sh
set -eu

# For a single-instance deployment this applies migrations before serving traffic.
# For multi-replica deployments, run migrations as a separate release job.
uv run --no-sync alembic upgrade head
uv run --no-sync python -m app.db.seed
exec uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port 8000
