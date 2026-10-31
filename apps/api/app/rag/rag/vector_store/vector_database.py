"""Persistent Chroma vector store. Embeddings are created by our own model."""
import chromadb

from rag.config import settings


class TourismVectorStore:
    def __init__(self) -> None:
        settings.chroma_dir.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(settings.chroma_dir))
        self.collection = self.client.get_or_create_collection(
            name=settings.collection_name,
            configuration={"hnsw": {"space": "cosine"}},
            metadata={"description": "Yatranook Odisha tourism knowledge base"},
        )

    def replace_source(
        self,
        source: str,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        # Remove old chunks for this file so re-ingestion does not leave stale chunks.
        self.collection.delete(where={"source": source})
        if ids:
            self.collection.upsert(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas,
            )

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        if self.collection.count() == 0:
            return []
        result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        matches = []
        for index, document in enumerate(result["documents"][0]):
            distance = result["distances"][0][index]
            matches.append({
                "text": document,
                "metadata": result["metadatas"][0][index] or {},
                "distance": float(distance),
                "similarity": 1.0 - float(distance),
            })
        return matches

    def count(self) -> int:
        return self.collection.count()
