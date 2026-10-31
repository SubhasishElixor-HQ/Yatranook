"""Ingest all supported tourism files into Chroma."""
import hashlib
from pathlib import Path

from rag.config import settings
from rag.embeddings.embedding_generator import embed_documents
from rag.ingestion.document_loader import load_directory
from rag.preprocessing.chunking import chunk_document
from rag.vector_store.vector_database import TourismVectorStore


def ingest_data(data_dir: Path | None = None) -> int:
    data_dir = data_dir or settings.data_dir
    documents = load_directory(data_dir)
    if not documents:
        raise RuntimeError(
            f"No readable TXT, MD, JSON or PDF documents found in {data_dir}. "
            "Add tourism information before running ingestion."
        )

    store = TourismVectorStore()
    # Ingest each source separately, so updating one file replaces its old chunks.
    grouped: dict[str, list] = {}
    for document in documents:
        grouped.setdefault(document.source, []).append(document)

    total_chunks = 0
    for source, source_documents in grouped.items():
        chunks = []
        for document in source_documents:
            chunks.extend(
                chunk_document(document, settings.chunk_size, settings.chunk_overlap)
            )
        texts = [chunk.text for chunk in chunks]
        vectors = embed_documents(texts)
        ids = [
            hashlib.sha256(
                f"{source}|{i}|{chunk.text}".encode("utf-8")
            ).hexdigest()
            for i, chunk in enumerate(chunks)
        ]
        metadatas = []
        for chunk in chunks:
            # Chroma metadata supports scalar values; stringify unexpected values.
            metadata = {}
            for key, value in chunk.metadata.items():
                if isinstance(value, (str, int, float, bool)):
                    metadata[key] = value
                elif value is not None:
                    metadata[key] = str(value)
            metadatas.append(metadata)
        store.replace_source(source, ids, texts, vectors, metadatas)
        total_chunks += len(chunks)
        print(f"Indexed {len(chunks):>4} chunks from {source}")

    print(f"Done. Total chunks indexed: {total_chunks}")
    return total_chunks
