import json
from pathlib import Path

from rag.ingestion.document_loader import load_file


def test_json_records_are_loaded(tmp_path: Path):
    path = tmp_path / "places.json"
    path.write_text(json.dumps([
        {"place": "Sample Place", "content": "A sample description."}
    ]), encoding="utf-8")
    docs = load_file(path, tmp_path)
    assert len(docs) == 1
    assert "A sample description" in docs[0].text
    assert docs[0].metadata["place"] == "Sample Place"
