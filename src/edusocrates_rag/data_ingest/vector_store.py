# src/edusocrates_rag/data_ingest/vector_store.py
"""
Build / update a FAISS index from chunks produced
by ingest.py  ──>  <kb>/faiss.index  +  <kb>/chunks.json
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict

import faiss                   # pip install faiss-cpu
from sentence_transformers import SentenceTransformer

# ─────────────────────────────────────────────── globals
_EMBED_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
_DIM = _EMBED_MODEL.get_sentence_embedding_dimension()


# ─────────────────────────────────────────────── api
def build_index(
    chunks: List[Dict],
    kb_path: Path,
    index_name: str = "faiss.index",
) -> None:
    """
    chunks  : list returned by data_ingest.ingest.ingest_file()
    kb_path : path to knowledge-base folder (…/knowledge/<KB>)
    """
    kb_path.mkdir(parents=True, exist_ok=True)
    vecs = _EMBED_MODEL.encode([c["text"] for c in chunks]).astype("float32")

    index = faiss.IndexFlatIP(_DIM)
    index.add(vecs)  # type: ignore[arg-type]

    # save index
    faiss.write_index(index, str(kb_path / index_name))

    # also persist metadata so we can map id → chunk
    with open(kb_path / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"💾💥 Saved {len(chunks)} vectors → {kb_path / index_name}")


def load_index(kb_path: Path, index_name: str = "faiss.index"):
    """Return (faiss_index, chunks_metadata_list)."""
    index = faiss.read_index(str(kb_path / index_name))
    with open(kb_path / "chunks.json", encoding="utf-8") as f:
        meta = json.load(f)
    return index, meta


def search(
    question: str,
    kb_path: Path,
    top_k: int = 5,
) -> List[Dict]:
    """Return top-k chunk dicts with extra 'score' field."""
    index, meta = load_index(kb_path)
    q_vec = _EMBED_MODEL.encode([question]).astype("float32")
    scores, ids = index.search(q_vec, top_k)
    results = []
    for score, idx in zip(scores[0], ids[0]):
        if idx == -1:
            continue
        c = meta[idx].copy()
        c["score"] = float(score)
        results.append(c)
    return results
