# tests/test_vector_store.py
from pathlib import Path
from edusocrates_rag.data_ingest.ingest import ingest_pdf
from edusocrates_rag.data_ingest.vector_store import build_index, search

def test_retrieve_gradient(tmp_path):
    pdf = Path("datas/PDFs/DeepLearning/Sách Deep Learning cơ bản - v2.pdf")
    chunks = ingest_pdf(pdf)
    kb = tmp_path / "kb"
    build_index(chunks, kb)
    hits = search("gradient descent", kb, top_k=3)
    assert hits, "No passage retrieved"
    assert any("gradient" in h["text"].lower() for h in hits)
