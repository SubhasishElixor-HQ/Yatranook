from rag.ingestion.document_loader import LoadedDocument
from rag.preprocessing.chunking import chunk_document


def test_chunk_document_respects_requested_size():
    document = LoadedDocument("word " * 500, "sample.txt")
    chunks = chunk_document(document, chunk_size=300, overlap=40)
    assert len(chunks) > 1
    assert all(len(chunk.text) <= 300 for chunk in chunks)
    assert all(chunk.metadata["source"] == "sample.txt" for chunk in chunks)


def test_empty_document_returns_no_chunks():
    document = LoadedDocument("   ", "empty.txt")
    assert chunk_document(document) == []
