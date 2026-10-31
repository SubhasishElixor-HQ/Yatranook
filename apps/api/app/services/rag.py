import logging

import httpx
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.tourism_document import TourismDocument

logger = logging.getLogger(__name__)


async def create_embedding(text: str) -> list[float] | None:
    url = f"{settings.ollama_base_url.rstrip('/')}/api/embed"
    payload = {"model": settings.ollama_embedding_model, "input": text}
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        embedding = response.json()["embeddings"][0]
        if len(embedding) != settings.embedding_dimensions:
            logger.warning(
                "Ollama embedding dimension %s does not match pgvector dimension %s; using keyword retrieval",
                len(embedding),
                settings.embedding_dimensions,
            )
            return None
        return embedding


async def retrieve_tourism_context(db: Session, query: str, limit: int = 5) -> list[dict]:
    embedding = None
    try:
        embedding = await create_embedding(query)
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError):
        logger.warning("Ollama embedding provider unavailable; falling back to keyword retrieval", exc_info=True)

    if embedding:
        statement = (
            select(TourismDocument)
            .where(TourismDocument.embedding.is_not(None))
            .order_by(TourismDocument.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        documents = list(db.scalars(statement).all())
    else:
        terms = [term.strip() for term in query.split() if len(term.strip()) >= 3][:12]
        filters = [
            field.ilike(f"%{term}%")
            for term in terms
            for field in (TourismDocument.title, TourismDocument.content)
        ]
        statement = (
            select(TourismDocument)
            .where(or_(*filters))
            .order_by(TourismDocument.created_at.desc())
            .limit(limit)
        )
        documents = list(db.scalars(statement).all())

    return [
        {
            "title": item.title,
            "content": item.content[:1800],
            "source_name": item.source_name,
            "source_url": item.source_url,
        }
        for item in documents
    ]
