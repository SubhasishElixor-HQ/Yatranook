# Adding the RAG module to Yatranook-Production

I could not see `apps/api` (only compose, README, env and docs were uploaded), so these files are written against
what the README describes: FastAPI, SQLAlchemy with `postgresql+psycopg`, Alembic, pgvector, Ollama.

1. Copy `apps/api/app/rag/` into your `apps/api/app/`.
2. Copy `apps/api/migrations/20261031_rag_tables.py` into your Alembic versions folder, set `down_revision`
   (`uv run alembic heads`), then `uv run alembic upgrade head`.
3. In `main.py`:
   ```python
   from app.rag.router import build_router
   from app.db.session import get_db   # use your real session dependency
   app.include_router(build_router(get_db), prefix="/api/v1")
   ```
   New routes: `POST /api/v1/assistant/turns` and `POST /api/v1/assistant/itinerary`. Keep `/assistant/chat` and `/assistant/plan` until the frontend switches.
4. `ollama pull llama3.2:3b` and `ollama pull nomic-embed-text`, then set `OLLAMA_CHAT_MODEL=llama3.2:3b`.
5. Ingest and approve (from `apps/api`):
   ```bash
   uv run python -m app.rag.ingest ../../data/odisha_seed.jsonl
   uv run python -m app.rag.ingest --approve "https://whc.unesco.org/en/list/246/" --reviewer "your name"
   ```
   Review each record against its source first; set `last_verified` in the JSONL once you have checked it.
6. Tests: copy `tests/rag/` and run `uv run pytest tests/rag`.
7. Evaluate: `uv run python -m scripts.eval_rag ../../eval/rag_eval_set.jsonl > report.json`.
8. Inside Docker the API reaches Ollama through `host.docker.internal` (already set in your compose file).

Example calls:
```bash
curl -X POST localhost:8080/api/v1/assistant/turns -H 'content-type: application/json' \
  -d '{"message":"Which dynasty built the Konark Sun Temple?"}'

curl -X POST localhost:8080/api/v1/assistant/itinerary -H 'content-type: application/json' \
  -d '{"trip":{"destination_scope":["Puri"],"duration_days":2,"budget_inr":3000,"budget_includes_transport":false,"interests":["temples","beaches"]}}'
```
