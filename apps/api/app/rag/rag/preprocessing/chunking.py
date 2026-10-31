"""Split documents into overlapping, word-safe chunks."""
from dataclasses import dataclass
from typing import Any

from rag.ingestion.document_loader import LoadedDocument
from rag.preprocessing.text_cleaner import clean_text


@dataclass
class TextChunk:
    text: str
    metadata: dict[str, Any]


def chunk_document(
    document: LoadedDocument, chunk_size: int = 900, overlap: int = 150
) -> list[TextChunk]:
    if chunk_size < 100:
        raise ValueError("chunk_size should be at least 100 characters")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

    text = clean_text(document.text)
    if not text:
        return []

    chunks: list[TextChunk] = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            # Prefer ending at a word boundary.
            boundary = text.rfind(" ", start, end)
            if boundary > start + chunk_size // 2:
                end = boundary
        piece = text[start:end].strip()
        if piece:
            metadata = dict(document.metadata)
            metadata.update({"source": document.source, "chunk_index": len(chunks)})
            chunks.append(TextChunk(piece, metadata))
        if end >= len(text):
            break
        next_start = max(start + 1, end - overlap)
        # Avoid starting in the middle of a word.
        next_space = text.find(" ", next_start, min(next_start + 30, len(text)))
        start = next_space + 1 if next_space != -1 else next_start
    return chunks
