"""Public interface for other Yatranook components to call."""
from rag.generation.response_generator import generate_response
from rag.retrieval.retriever import retrieve


def answer_question(question: str, top_k: int = 5) -> dict:
    """Return an answer and source references for a user question.

    This function is the integration point for the backend developer.
    """
    matches = retrieve(question, top_k=top_k)
    answer = generate_response(question, matches)
    sources = []
    for match in matches:
        metadata = match.get("metadata", {})
        sources.append({
            "source": metadata.get("source", "Unknown source"),
            "place": metadata.get("place") or metadata.get("destination"),
            "category": metadata.get("category"),
            "reference": metadata.get("reference") or metadata.get("url"),
            "similarity": round(match["similarity"], 4),
            "excerpt": match["text"][:240],
        })
    return {"answer": answer, "sources": sources}
