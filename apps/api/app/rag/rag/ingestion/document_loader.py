"""Load TXT, Markdown, JSON and PDF files into standard document records."""
from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pypdf import PdfReader


@dataclass
class LoadedDocument:
    text: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)


def _json_to_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("documents", "items", "places", "destinations", "records"):
            if isinstance(payload.get(key), list):
                return [item for item in payload[key] if isinstance(item, dict)]
        return [payload]
    raise ValueError("JSON must contain an object or a list of objects")


def _record_to_text(record: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    # Prefer explicit text-like fields, then include other scalar fields as context.
    content_keys = ("content", "text", "description", "details", "overview")
    content = next(
        (str(record[key]).strip() for key in content_keys
         if record.get(key) is not None and str(record[key]).strip()),
        "",
    )
    lines: list[str] = []
    for key, value in record.items():
        if value is None or isinstance(value, (dict, list)):
            continue
        value_text = str(value).strip()
        if not value_text:
            continue
        if key in content_keys:
            continue
        lines.append(f"{key.replace('_', ' ').title()}: {value_text}")
    if content:
        lines.append(content)
    text = "\n".join(lines).strip()
    metadata = {}
    for key in ("place", "destination", "category", "district", "url"):
        value = record.get(key)
        if isinstance(value, (str, int, float, bool)):
            metadata[key] = value
    # Keep the human-readable citation separate from the source filename used
    # internally to replace/re-index one input file.
    reference = record.get("source")
    if isinstance(reference, (str, int, float, bool)):
        metadata["reference"] = reference
    return text, metadata


def load_file(path: Path, base_dir: Path | None = None) -> list[LoadedDocument]:
    """Load one supported file. PDF pages and JSON records become separate documents."""
    suffix = path.suffix.lower()
    source = str(path.relative_to(base_dir)) if base_dir else path.name

    if suffix in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        return [LoadedDocument(text, source)] if text else []

    if suffix == ".pdf":
        reader = PdfReader(str(path))
        documents = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if text:
                documents.append(
                    LoadedDocument(text, source, {"page": page_number})
                )
        return documents

    if suffix == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        documents = []
        for index, record in enumerate(_json_to_records(payload), start=1):
            text, metadata = _record_to_text(record)
            if text:
                metadata["record"] = index
                documents.append(LoadedDocument(text, source, metadata))
        return documents

    raise ValueError(f"Unsupported file type: {suffix}. Use TXT, MD, JSON or PDF.")


def load_directory(directory: Path) -> list[LoadedDocument]:
    if not directory.exists():
        raise FileNotFoundError(f"Tourism data directory does not exist: {directory}")
    allowed = {".txt", ".md", ".json", ".pdf"}
    documents: list[LoadedDocument] = []
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.suffix.lower() in allowed:
            documents.extend(load_file(path, directory))
    return documents
