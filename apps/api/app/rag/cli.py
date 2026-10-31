"""Command-line interface for indexing data and asking questions."""
import argparse
import json

from rag.config import settings
from rag.ingestion.ingest import ingest_data
from rag.rag_pipeline import answer_question
from rag.retrieval.retriever import retrieve


def main() -> None:
    parser = argparse.ArgumentParser(description="Yatranook RAG tools")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("ingest", help="Load tourism files into Chroma")
    ask_parser = subparsers.add_parser("ask", help="Ask a tourism question")
    ask_parser.add_argument("question", help="Question to ask")
    ask_parser.add_argument("--top-k", type=int, default=settings.top_k)
    search_parser = subparsers.add_parser(
        "search", help="Test retrieval without calling Gemini"
    )
    search_parser.add_argument("question", help="Question to search")
    search_parser.add_argument("--top-k", type=int, default=settings.top_k)
    args = parser.parse_args()

    if args.command == "ingest":
        ingest_data()
    elif args.command == "search":
        matches = retrieve(args.question, args.top_k)
        print(json.dumps(matches, ensure_ascii=False, indent=2))
    elif args.command == "ask":
        print(json.dumps(
            answer_question(args.question, args.top_k), ensure_ascii=False, indent=2
        ))


if __name__ == "__main__":
    main()
