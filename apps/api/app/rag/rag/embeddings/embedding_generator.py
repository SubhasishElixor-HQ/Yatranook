"""Local sentence-transformer embeddings for documents and queries."""
from functools import lru_cache
from sentence_transformers import SentenceTransformer

from rag.config import settings


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    # The model is downloaded on first run and cached by Hugging Face locally.
    return SentenceTransformer(settings.embedding_model)


def embed_documents(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_model().encode_document(
        texts, normalize_embeddings=True, show_progress_bar=False
    )
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    vector = get_model().encode_query(text, normalize_embeddings=True)
    return vector.tolist()
