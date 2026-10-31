"""Small manual retrieval evaluation helper; it does not call the LLM."""
from rag.retrieval.retriever import retrieve


def evaluate_queries(queries: list[str], top_k: int = 5) -> None:
    for query in queries:
        print(f"\nQUESTION: {query}")
        matches = retrieve(query, top_k=top_k)
        if not matches:
            print("  No documents indexed.")
            continue
        for rank, match in enumerate(matches, start=1):
            metadata = match["metadata"]
            print(
                f"  {rank}. {metadata.get('source', 'unknown')} | "
                f"similarity={match['similarity']:.3f}"
            )
            print(f"     {match['text'][:180]}...")


if __name__ == "__main__":
    evaluate_queries([
        "What can visitors see in Puri?",
        "Tell me about the Sun Temple at Konark.",
        "Which local food should I try in Odisha?",
    ])
