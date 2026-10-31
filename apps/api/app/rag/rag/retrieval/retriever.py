"""Retrieve the most semantically relevant tourism chunks."""
from rag.config import settings
from rag.embeddings.embedding_generator import embed_query
from rag.vector_store.vector_database import TourismVectorStore


def retrieve(query: str, top_k: int | None = None) -> list[dict]:
    query = query.strip()
    if not query:
        raise ValueError("Query cannot be empty")
    store = TourismVectorStore()
    return store.search(embed_query(query), top_k or settings.top_k)
