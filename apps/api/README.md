# Yatranook FastAPI

Python 3.12+, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL/pgvector, Pydantic Settings, JWT access tokens.

The checked-in `.python-version` pins local `uv` commands to Python 3.12. This avoids
Windows Application Control issues with compiled dependencies under newer, unapproved
Python runtimes.

Run from this directory:

```bash
uv sync --extra dev
uv run alembic upgrade head
uv run python -m app.db.seed
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Tests and checks:

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

The `scripts/ingest_documents.py` command ingests JSONL source documents. See the root README for schema and data governance expectations.
