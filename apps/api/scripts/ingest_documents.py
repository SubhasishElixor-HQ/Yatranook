"""Ingest newline-delimited JSON tourism documents into PostgreSQL.

Expected JSONL fields: title, content, source_name, optional source_url, optional metadata.
Use only content you have permission to store and retrieve.
"""

import argparse
import asyncio
import json
from pathlib import Path

from app.db.session import SessionLocal
from app.models.tourism_document import TourismDocument
from app.services.rag import create_embedding


async def ingest(path: Path) -> int:
    count = 0
    with SessionLocal() as db, path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            item = json.loads(line)
            required = ("title", "content", "source_name")
            if any(not str(item.get(field, "")).strip() for field in required):
                raise ValueError(
                    f"Line {line_number}: title, content, and source_name are required"
                )
            content = str(item["content"]).strip()
            embedding = await create_embedding(f"{item['title']}\n{content}")
            document = TourismDocument(
                title=str(item["title"]).strip(),
                content=content,
                source_name=str(item["source_name"]).strip(),
                source_url=item.get("source_url"),
                metadata_json=item.get("metadata", {}),
                embedding=embedding,
            )
            db.add(document)
            count += 1
        db.commit()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest tourism knowledge JSONL")
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    total = asyncio.run(ingest(args.file))
    print(f"Ingested {total} tourism documents")
    if total:
        print(
            "Note: Ollama embeddings are generated when the configured Ollama server and model are available; otherwise keyword retrieval is used."
        )


if __name__ == "__main__":
    main()
